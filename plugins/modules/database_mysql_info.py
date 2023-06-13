#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode MySQL Managed Database."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_mysql as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_mysql_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import (
    call_protected_provisioning,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    mapping_to_dict,
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import MySQLDatabase

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.string,
        conflicts_with=["label"],
        description=["The ID of the MySQL Database."],
    ),
    "label": SpecField(
        type=FieldType.string,
        conflicts_with=["id"],
        description=["The label of the MySQL Database."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode MySQL Managed Database."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "database": SpecReturnValue(
            description="The database in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/databases/"
            "#managed-mysql-database-view__response-samples",
            type=FieldType.dict,
            sample=docs_parent.result_database_samples,
        ),
        "backups": SpecReturnValue(
            description="The database backups in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/databases/"
            "#managed-mysql-database-backup-view__responses",
            type=FieldType.dict,
            sample=docs_parent.result_backups_samples,
        ),
        "ssl_cert": SpecReturnValue(
            description="The SSL CA certificate for an accessible Managed MySQL Database.",
            docs_url="https://www.linode.com/docs/api/databases/"
            "#managed-mysql-database-ssl-certificate-view__responses",
            type=FieldType.dict,
            sample=docs_parent.result_ssl_cert_samples,
        ),
        "credentials": SpecReturnValue(
            description="The root username and password for an accessible Managed MySQL Database.",
            docs_url="https://www.linode.com/docs/api/databases/"
            "#managed-mysql-database-credenti"
            "als-view__responses",
            type=FieldType.dict,
            sample=docs_parent.result_credentials_samples,
        ),
    },
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "database": None,
            "backups": None,
            "credentials": None,
            "ssl_cert": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
            mutually_exclusive=[("id", "label")],
        )

    def _get_database_by_label(self, label: str) -> Optional[MySQLDatabase]:
        try:
            resp = [
                db
                for db in self.client.database.mysql_instances()
                if db.label == label
            ]

            return resp[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get database {0}: {1}".format(label, exception)
            )

    def _get_database_by_id(self, database_id: int) -> MySQLDatabase:
        return self._get_resource_by_id(MySQLDatabase, database_id)

    def _write_result(self, database: MySQLDatabase) -> None:
        # Force lazy-loading
        database._api_get()

        self.results["database"] = database._raw_json
        self.results["backups"] = call_protected_provisioning(
            lambda: paginated_list_to_json(database.backups)
        )
        self.results["credentials"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.credentials)
        )
        self.results["ssl_cert"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.ssl)
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for database info module"""

        params = filter_null_values(self.module.params)

        if "id" in params:
            self._write_result(self._get_database_by_id(params.get("id")))

        if "label" in params:
            self._write_result(self._get_database_by_label(params.get("label")))

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
