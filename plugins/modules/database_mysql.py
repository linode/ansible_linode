#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Images."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
import os
from typing import Optional, cast, Any, Set, Dict

import polling
import requests
from linode_api4 import LinodeClient, ApiError

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    handle_updates, filter_null_values, handle_updates_resource

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image as docs

from ansible_collections.linode.cloud.plugins.module_utils.linode_objects import MySQLDatabase

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
            'Each item can be a single IP address or a range in CIDR format.'
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
        image=dict(
            description='The database in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-mysql-database-view__response-samples',
            type='dict',
            sample=docs.result_image_samples
        )
    )
)

MUTABLE_FIELDS = {
    'allow_list',
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
            resp = self.client.get('/databases/mysql/instances')

            dbs = [v for v in resp['data'] if v['label'] == label]

            return MySQLDatabase(self.client, dbs[0]['id'], data=dbs[0])
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get database {0}: {1}'.format(label, exception))

    def _wait_for_database_status(self, database: MySQLDatabase, status: Set[str]) -> None:
        def poll_func() -> bool:
            database.api_get()
            return database.data['status'] in status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=10,
                timeout=self.module.params.get('wait_timeout'),
            )
        except polling.TimeoutException:
            self.fail('failed to wait for database status: timeout period expired')

    def _create_database(self) -> Optional[MySQLDatabase]:
        params = self.module.params
        create_params = {
            'allow_list', 'cluster_size', 'encrypted',
            'engine', 'label', 'region', 'replication_type',
            'ssl_connection', 'type'
        }

        request_body = {k: v for k, v in params.items() if k in create_params and k is not None}

        resp = self.client.post('/databases/mysql/instances', data=request_body)

        return MySQLDatabase(self.client, resp['id'], data=resp)

    def _update_database(self, db: MySQLDatabase) -> None:
        db.api_get()

        exceptions = {'allow_list'}

        params_filtered = {k: v for k, v in filter_null_values(self.module.params).items() if k not in exceptions}

        handle_updates_resource(db, params_filtered, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get('label')

        db = self._get_database_by_label(label)

        # Create the database if it does not already exist
        if db is None:
            db = self._create_database()
            self.register_action('Created database {0}'.format(label))

        self._update_database(db)

        # Force lazy-loading
        db.api_get()

        self.results['database'] = db.data
        self.results['backups'] = db.get_backups()
        self.results['credentials'] = db.get_credentials()
        self.results['ssl_cert'] = db.get_ssl_cert()

    def _handle_absent(self) -> None:
        label: str = self.module.params.get('label')

        db = self._get_database_by_label(label)

        if db is not None:
            self.results['database'] = db.data
            self.results['backups'] = db.get_backups()
            self.results['credentials'] = db.get_credentials()
            self.results['ssl_cert'] = db.get_ssl_cert()

            self.client.delete('/databases/mysql/instances/{}'.format(db.id))
            self.register_action('Deleted database {0}'.format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Image module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Image module"""
    Module()


if __name__ == '__main__':
    main()
