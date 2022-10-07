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
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import \
    validate_shared_db_input, call_protected_provisioning, SPEC_UPDATE_WINDOW

from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    handle_updates, filter_null_values, paginated_list_to_json, mapping_to_dict, poll_condition

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_mysql as docs

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
            'Defaults to none for a single cluster and '
            'semi_synch for a high availability cluster.',
            'Must be none for a single node cluster.',
            'Must be asynch or semi_synch for a high availability cluster.'
        ],
        choices=['none', 'asynch', 'semi_synch'],
        default='none'
    ),
    ssl_connection=dict(
        type='bool',
        description='Whether to require SSL credentials to '
                    'establish a connection to the Managed Database.',
        default=True,
    ),
    type=dict(
        type='str',
        description='The Linode Instance type used by the '
                    'Managed Database for its nodes.',
    ),
    updates=dict(
        type='dict',
        options=SPEC_UPDATE_WINDOW,
        description='Configuration settings for automated patch '
                    'update maintenance for the Managed Database.'
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

    def _get_database_by_label(self, label: str) -> Optional[MySQLDatabase]:
        try:
            resp = [db for db in self.client.database.mysql_instances() if db.label == label]

            return resp[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get database {0}: {1}'.format(label, exception))

    @staticmethod
    def _wait_for_database_status(database: MySQLDatabase,
                                  status: Set[str], step: int, timeout: int) -> None:
        def condition_func() -> bool:
            database._api_get()
            return database.status in status

        poll_condition(condition_func, step, timeout)

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
            return self.fail(msg='Failed to create database: {}'.format('; '.join(err.errors)))

    def _update_database(self, database: MySQLDatabase) -> None:
        try:
            database._api_get()

            params = filter_null_values(self.module.params)

            # Engine is input as a slug
            if 'engine' in params:
                params['engine'] = params['engine'].split('/')[0]

            try:
                changed_fields = handle_updates(
                    database, params, MUTABLE_FIELDS, self.register_action)
            except Exception as err:
                self.fail(msg='Failed to update database: {}'.format(err))

            # We only want to wait on fields that trigger an update
            if len(changed_fields) > 0 and self.module.params['wait']:
                try:
                    self._wait_for_database_status(database, {'updating'}, 1, 4)
                except polling.TimeoutException:
                    # Only certain field updates will trigger an update event.
                    # Assume the database will not enter an updating status
                    # if the status has not updated at this point.
                    pass
                except Exception as err:
                    self.fail(msg='failed to wait for database updating: {}'.format(err))

                try:
                    self._wait_for_database_status(database, {'active'}, 4, 240)
                except Exception as err:
                    self.fail(msg='failed to wait for database active: {}'.format(err))
        except ApiError as err:
            self.fail(msg='Failed to update database: {}'.format('; '.join(err.errors)))

    def _write_result(self, database: MySQLDatabase) -> None:
        # Force lazy-loading
        database._api_get()

        self.results['database'] = database._raw_json
        self.results['backups'] = call_protected_provisioning(
            lambda: paginated_list_to_json(database.backups))
        self.results['credentials'] = call_protected_provisioning(
            lambda: mapping_to_dict(database.credentials))
        self.results['ssl_cert'] = call_protected_provisioning(
            lambda: mapping_to_dict(database.ssl))

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get('label')

        database = self._get_database_by_label(label)

        # Create the database if it does not already exist
        if database is None:
            database = self._create_database()
            self.register_action('Created database {0}'.format(label))

        if params.get('wait'):
            try:
                self._wait_for_database_status(database, {'active'}, 4, params.get('wait_timeout'))
            except Exception as err:
                self.fail(msg='failed to wait for database active: {}'.format(err))

        self._update_database(database)

        self._write_result(database)

    def _handle_absent(self) -> None:
        label: str = self.module.params.get('label')

        database = self._get_database_by_label(label)

        if database is not None:
            self._write_result(database)

            database.delete()
            self.register_action('Deleted database {0}'.format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for MySQL module"""

        try:
            validate_shared_db_input(self.module.params)
        except ValueError as err:
            self.fail(msg='Invalid param: {}'.format(err))

        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the database_mysql module"""
    Module()


if __name__ == '__main__':
    main()
