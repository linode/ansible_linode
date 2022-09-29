#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Images."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
import os
from typing import Optional, cast, Any, Set, Dict, Callable

import polling
import requests
from linode_api4 import LinodeClient, ApiError
from linode_api4.objects import MySQLDatabase

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    handle_updates, filter_null_values, paginated_list_to_json, mapping_to_dict

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_mysql as docs

SPEC_UPDATES = dict(
    day_of_week=dict(
        type='int',
        required=True,
        choices=range(1, 7),
        description='The day to perform maintenance. 1=Monday, 2=Tuesday, etc.'
    ),
    duration=dict(
        type='int',
        required=True,
        choices=range(1, 3),
        description='The maximum maintenance window time in hours.'
    ),
    frequency=dict(
        type='str',
        choices=['weekly', 'monthly'],
        default='weekly',
        description='Whether maintenance occurs on a weekly or monthly basis.'
    ),
    hour_of_day=dict(
        type='int',
        required=True,
        description='The hour to begin maintenance based in UTC time.',
    ),
    week_of_month=dict(
        type='int',
        description=[
            'The week of the month to perform monthly frequency updates.',
            'Defaults to None.',
            'Required for monthly frequency updates.',
            'Must be null for weekly frequency updates.'
        ]
    )
)

SPEC = dict(
    label=dict(
        type='str',
        required=True,
        description='This database\'s unique label.'),
    state=dict(
        type='str',
        choices=['present', 'absent'],
        required=True,
        description='The state of this database.',
    ),

    allow_list=dict(
        type='list',
        elements='str',
        description=[
            'A list of IP addresses that can access the Managed Database.',
            'Each item must be a range in CIDR format.'
        ],
        default=[]
    ),
    cluster_size=dict(
        type='int',
        description='The number of Linode Instance nodes deployed to the Managed Database.',
        choices=[1, 3],
        default=1
    ),
    encrypted=dict(
        type='bool',
        description='Whether the Managed Databases is encrypted.',
    ),
    engine=dict(
        type='str',
        description='The Managed Database engine in engine/version format.',
    ),
    region=dict(
        type='str',
        description='The Region ID for the Managed Database.'
    ),
    replication_type=dict(
        type='str',
        description=[
            'The replication method used for the Managed Database.',
            'Defaults to none for a single cluster and semi_synch for a high availability cluster.',
            'Must be none for a single node cluster.',
            'Must be asynch or semi_synch for a high availability cluster.'
        ],
        choices=['none', 'asynch', 'semi_synch'],
        default='none'
    ),
    ssl_connection=dict(
        type='bool',
        description='Whether to require SSL credentials to establish a connection to the Managed Database.',
        default=True,
    ),
    type=dict(
        type='str',
        description='The Linode Instance type used by the Managed Database for its nodes.',
    ),
    updates=dict(
        type='dict',
        options=SPEC_UPDATES,
        description='Configuration settings for automated patch update maintenance for the Managed Database.'
    ),
    wait=dict(
        type='bool', default=True,
        description='Wait for the database to have status `available` before returning.'),

    wait_timeout=dict(
        type='int', default=3600,
        description='The amount of time, in seconds, to wait for an image to '
                    'have status `available`.'
    ),
)

specdoc_meta = dict(
    description=[
        'Manage a Linode MySQL database.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=SPEC,
    examples=docs.specdoc_examples,
    return_values=dict(
        database=dict(
            description='The database in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-mysql-database-view__response-samples',
            type='dict',
            sample=docs.result_database_samples
        ),
        backups=dict(
            description='The database backups in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-mysql-database-backup-view__responses',
            type='dict',
            sample=docs.result_backups_samples
        ),
        ssl_cert=dict(
            description='The SSL CA certificate for an accessible Managed MySQL Database.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-mysql-database-ssl-certificate-view__responses',
            type='dict',
            sample=docs.result_ssl_cert_samples
        ),
        credentials=dict(
            description='The root username and password for an accessible Managed MySQL Database.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-mysql-database-credentials-view__responses',
            type='dict',
            sample=docs.result_credentials_samples
        ),
    )
)

MUTABLE_FIELDS = {
    'allow_list',
    'updates'
}


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Databases"""

    def __init__(self) -> None:
        self.module_arg_spec = SPEC
        self.results = dict(
            changed=False,
            actions=[],
            database=None,
            backups=None,
            credentials=None,
            ssl_cert=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=[('state', 'label')],
                         required_if=[('state', 'present', ['region', 'engine', 'type'], True)])

    @staticmethod
    def _call_protected_provisioning(func: Callable) -> Optional[Any]:
        """
        Helper function to return None on requests made while a database is provisioning.
        """
        try:
            return func()
        except ApiError as err:
            if err.status == 400:
                # Database is provisioning
                return None

            raise err

    def _get_database_by_label(self, label: str) -> Optional[MySQLDatabase]:
        try:
            resp = [db for db in self.client.database.mysql_instances() if db.label == label]

            return resp[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get database {0}: {1}'.format(label, exception))

    def _wait_for_database_status(self, database: MySQLDatabase, status: Set[str]) -> None:
        def poll_func() -> bool:
            database._api_get()
            return database.status in status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=4,
                timeout=self.module.params.get('wait_timeout'),
            )
        except polling.TimeoutException:
            self.fail('failed to wait for database status: timeout period expired')

    def _create_database(self) -> Optional[MySQLDatabase]:
        params = self.module.params

        create_params = {
            'allow_list', 'cluster_size', 'encrypted', 'replication_type', 'ssl_connection'
        }

        additional_args = {k: v for k, v in params.items() if k in create_params and k is not None}

        try:
            return self.client.database.mysql_create(
                params.get('label'),
                params.get('region'),
                params.get('engine'),
                params.get('type'),
                **additional_args
            )
        except ApiError as err:
            self.fail(msg='Failed to create database: {}'.format('; '.join(err.errors)))

    def _update_database(self, db: MySQLDatabase) -> None:
        try:
            db._api_get()

            params = filter_null_values(self.module.params)

            # Engine is input as a slug
            if 'engine' in params:
                params['engine'] = params['engine'].split('/')[0]

            changed = handle_updates(db, params, MUTABLE_FIELDS, self.register_action)

            if changed and self.module.params['wait']:
                self._wait_for_database_status(db, {'updating'})
                self._wait_for_database_status(db, {'active'})
        except ApiError as err:
            self.fail(msg='Failed to update database: {}'.format('; '.join(err.errors)))

    def _write_result(self, db: MySQLDatabase) -> None:
        # Force lazy-loading
        db._api_get()

        self.results['database'] = db._raw_json
        self.results['backups'] = self._call_protected_provisioning(lambda: paginated_list_to_json(db.backups))
        self.results['credentials'] = self._call_protected_provisioning(lambda: mapping_to_dict(db.credentials))
        self.results['ssl_cert'] = self._call_protected_provisioning(lambda: mapping_to_dict(db.ssl))

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get('label')

        db = self._get_database_by_label(label)

        # Create the database if it does not already exist
        if db is None:
            db = self._create_database()
            self.register_action('Created database {0}'.format(label))

        if params.get('wait'):
            self._wait_for_database_status(db, {'active'})

        self._update_database(db)

        self._write_result(db)

    def _handle_absent(self) -> None:
        label: str = self.module.params.get('label')

        db = self._get_database_by_label(label)

        if db is not None:
            self._write_result(db)

            db.delete()
            self.register_action('Deleted database {0}'.format(label))

    def _validate_params(self) -> None:
        params = self.module.params

        if 'allow_list' in params and params['allow_list'] is not None:
            for ip in params['allow_list']:
                if len(ip.split('/')) != 2:
                    self.fail(msg='Invalid CIDR format for IP {}'.format(ip))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for MySQL module"""
        try:
            self._validate_params()

            state = kwargs.get('state')

            if state == 'absent':
                self._handle_absent()
                return self.results

            self._handle_present()

            return self.results

        # We want API errors to be readable
        except ApiError as err:
            self.fail(msg='Received Linode API Error: {}'.format('; '.join(err.errors)))


def main() -> None:
    """Constructs and calls the database_mysql module"""
    Module()


if __name__ == '__main__':
    main()
