#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode PostgreSQL Managed Database."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import PostgreSQLDatabase

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import \
    call_protected_provisioning
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    filter_null_values, paginated_list_to_json, mapping_to_dict
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_postgresql \
    as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.\
    database_postgresql_info as docs

spec = dict(
    # Disable the default values
    state=dict(type='str', required=False, doc_hide=True),

    id=dict(type='str', description='The ID of the PostgreSQL Database.'),
    label=dict(type='str', description='The label of the PostgreSQL Database.'),
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode PostgreSQL Managed Database.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        database=dict(
            description='The database in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-postgresql-database-view__response-samples',
            type='dict',
            sample=docs_parent.result_database_samples
        ),
        backups=dict(
            description='The database backups in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-postgresql-database-backups-list__response-samples',
            type='dict',
            sample=docs_parent.result_backups_samples
        ),
        ssl_cert=dict(
            description='The SSL CA certificate for an accessible Managed PostgreSQL Database.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-postgresql-database-ssl-certificate-view',
            type='dict',
            sample=docs_parent.result_ssl_cert_samples
        ),
        credentials=dict(
            description='The root username and password for an accessible Managed '
                        'PostgreSQL Database.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-postgresql-database-credentials-view__request-samples',
            type='dict',
            sample=docs_parent.result_credentials_samples
        ),
    )
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode PostgreSQL database"""

    def __init__(self) -> None:
        self.module_arg_spec = spec
        self.results = {
            'database': None,
            'backups': None,
            'credentials': None,
            'ssl_cert': None,
        }

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=[('id', 'label')],
                         mutually_exclusive=[('id', 'label')])

    def _get_database_by_label(self, label: str) -> Optional[PostgreSQLDatabase]:
        try:
            resp = [db for db in self.client.database.postgresql_instances() if db.label == label]

            return resp[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get database {0}: {1}'.format(label, exception))

    def _get_database_by_id(self, database_id: int) -> PostgreSQLDatabase:
        return self._get_resource_by_id(PostgreSQLDatabase, database_id)

    def _write_result(self, database: PostgreSQLDatabase) -> None:
        # Force lazy-loading
        database._api_get()

        self.results['database'] = database._raw_json
        self.results['backups'] = call_protected_provisioning(
            lambda: paginated_list_to_json(database.backups))
        self.results['credentials'] = call_protected_provisioning(
            lambda: mapping_to_dict(database.credentials))
        self.results['ssl_cert'] = call_protected_provisioning(
            lambda: mapping_to_dict(database.ssl))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for database info module"""

        params = filter_null_values(self.module.params)

        if 'id' in params:
            self._write_result(self._get_database_by_id(params.get('id')))

        if 'label' in params:
            self._write_result(self._get_database_by_label(params.get('label')))

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == '__main__':
    main()
