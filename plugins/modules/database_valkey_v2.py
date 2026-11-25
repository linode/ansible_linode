#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the implementation for the linode.cloud.database_valkey_v2 module."""

import copy
from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_valkey_v2 as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import (
    SPEC_FORK_VALKEY,
    SPEC_UPDATE_WINDOW_V2,
    call_protected_provisioning,
    wait_for_database_status,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values_recursive,
    handle_updates,
    mapping_to_dict,
    poll_condition,
    safe_find,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ValkeyDatabase

SPEC_ENGINE_CONFIG = {
    "backup_hour": SpecField(
        type=FieldType.integer,
        description=["The hour of day (UTC) when the backup starts."],
    ),
    "backup_minute": SpecField(
        type=FieldType.integer,
        description=["The minute of the hour when the backup starts."],
    ),
    "frequent_snapshots": SpecField(
        type=FieldType.bool,
        description=["Enable frequent local RDB snapshots."],
    ),
    "valkey_acl_channels_default": SpecField(
        type=FieldType.string,
        choices=["allchannels", "resetchannels"],
        description=["The default ACL for pub/sub channels."],
    ),
    "valkey_active_expire_effort": SpecField(
        type=FieldType.integer,
        description=["The effort used to expire active keys."],
    ),
    "valkey_activedefrag": SpecField(
        type=FieldType.bool,
        description=["Enable active memory defragmentation."],
    ),
    "valkey_lfu_decay_time": SpecField(
        type=FieldType.integer,
        description=["The LFU counter decay time."],
    ),
    "valkey_lfu_log_factor": SpecField(
        type=FieldType.integer,
        description=["The LFU counter logarithm factor."],
    ),
    "valkey_maxmemory_policy": SpecField(
        type=FieldType.string,
        choices=[
            "noeviction",
            "allkeys-lru",
            "volatile-lru",
            "allkeys-random",
            "volatile-random",
            "volatile-ttl",
            "volatile-lfu",
            "allkeys-lfu",
        ],
        description=["The policy used when Valkey reaches maxmemory."],
    ),
    "valkey_number_of_databases": SpecField(
        type=FieldType.integer,
        description=[
            "The number of databases available in the Valkey instance."
        ],
    ),
    "valkey_persistence": SpecField(
        type=FieldType.string,
        choices=["off", "rdb"],
        description=[
            "The Valkey persistence mode.",
            "When set to off, backup scheduling and maintenance updates are "
            + "not supported.",
        ],
    ),
    "valkey_pubsub_client_output_buffer_limit": SpecField(
        type=FieldType.integer,
        description=["The pub/sub client output buffer limit."],
    ),
    "valkey_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The number of seconds before an idle client connection closes."
        ],
    ),
}

SPEC = {
    "state": SpecField(
        type=FieldType.string,
        choices=["resume", "suspend", "present", "absent"],
        required=True,
        description=["The desired state of the Managed Database."],
    ),
    "allow_list": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of IP addresses and CIDR ranges that can access the Managed Database."
        ],
        editable=True,
    ),
    "cluster_size": SpecField(
        type=FieldType.integer,
        description=[
            "The number of Linode instance nodes deployed to the Managed Database."
        ],
        editable=True,
    ),
    "engine": SpecField(
        type=FieldType.string,
        description=["The Managed Database engine in engine/version format."],
        editable=True,
    ),
    "engine_config": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_ENGINE_CONFIG,
        description=[
            "Various parameters used to configure this database's underlying engine.",
            "NOTE: If a configuration parameter is not current accepted by this field, "
            + "configure using the linode.cloud.api_request module.",
        ],
        editable=True,
    ),
    "label": SpecField(
        type=FieldType.string,
        description=["The label of the Managed Database."],
    ),
    "detach_private_network": SpecField(
        description=[
            "If true, the Managed Database will be detached from its current private network "
            + "when `private_network` is null.",
            "If the Managed Database is not currently attached to a private network or "
            + "the private_network field is specified, this option has no effect.",
            "This is not necessary when switching between VPC subnets.",
        ],
        type=FieldType.bool,
        default=False,
    ),
    "private_network": SpecField(
        description=[
            "Restricts access to this database using a virtual private cloud (VPC) "
            + "that you've configured in the region where the database will live."
        ],
        editable=True,
        type=FieldType.dict,
        suboptions={
            "vpc_id": SpecField(
                description=[
                    "The ID of the virtual private cloud (VPC) "
                    + "to restrict access to this database using"
                ],
                type=FieldType.integer,
                required=True,
            ),
            "subnet_id": SpecField(
                description=[
                    "The ID of the VPC subnet to restrict access "
                    + "to this database using."
                ],
                type=FieldType.integer,
                required=True,
            ),
            "public_access": SpecField(
                description=[
                    "Set to `true` to allow clients outside of the VPC to "
                    + "connect to the database using a public IP address."
                ],
                type=FieldType.bool,
                default=False,
            ),
        },
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The region of the Managed Database."],
    ),
    "type": SpecField(
        type=FieldType.string,
        description=[
            "The Linode Instance type used by the Managed Database for its nodes.",
            "Must support Valkey; see GET /databases/types.",
        ],
        editable=True,
    ),
    "fork": SpecField(
        type=FieldType.dict,
        description=[
            "Information about a Valkey database to fork from.",
            "restore_time must be one of the source database's "
            + "available_restore_times values.",
        ],
        suboptions=SPEC_FORK_VALKEY,
    ),
    "updates": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_UPDATE_WINDOW_V2,
        description=[
            "Configuration settings for automated patch "
            "update maintenance for the Managed Database."
        ],
        editable=True,
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The maximum number of seconds a poll operation can take before "
            "raising an error."
        ],
        default=45 * 60,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Create, read, and update a Linode Valkey database.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "database": SpecReturnValue(
            description="The database in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-valkey-instance",
            type=FieldType.dict,
            sample=docs.result_database_samples,
        ),
        "ssl_cert": SpecReturnValue(
            description="The SSL CA certificate for an accessible Managed Valkey Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-valkey-instance-ssl",
            type=FieldType.dict,
            sample=docs.result_ssl_cert_samples,
        ),
        "credentials": SpecReturnValue(
            description="The root username and password for an "
            "accessible Managed Valkey Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-valkey-instance-credentials",
            type=FieldType.dict,
            sample=docs.result_credentials_samples,
        ),
    },
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module implementation for database_valkey_v2."""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "database": None,
            "ssl_cert": None,
            "credentials": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def _create(self) -> ValkeyDatabase:
        params = filter_null_values_recursive(
            {
                k: v
                for k, v in self.module.params.items()
                if k
                in [
                    "allow_list",
                    "cluster_size",
                    "engine",
                    "engine_config",
                    "fork",
                    "label",
                    "private_network",
                    "region",
                    "type",
                ]
            }
        )

        updates = self.module.params.get("updates")

        # This is necessary because `type` is a Python-reserved keyword
        if "type" in params:
            params["ltype"] = params.pop("type")

        create_poller = self.client.polling.event_poller_create(
            "database", "database_create"
        )

        database = self.client.database.valkey_create(**params)

        create_poller.set_entity_id(database.id)
        create_poller.wait_for_next_event_finished(
            timeout=self._timeout_ctx.seconds_remaining
        )

        wait_for_database_status(
            self.client,
            database,
            "active",
            timeout=self._timeout_ctx.seconds_remaining,
        )

        # The `updates` field is not currently supported in the POST
        # request body.
        if updates is not None:
            database.updates = updates
            database.save()

            wait_for_database_status(
                self.client,
                database,
                "active",
                timeout=self._timeout_ctx.seconds_remaining,
            )

        return database

    def _update(self, database: ValkeyDatabase) -> None:
        database._api_get()

        params = copy.deepcopy(self.module.params)

        # The database PUT endpoint accepts `version` rather than `engine`
        engine = params.pop("engine", None)
        if engine is not None:
            engine_components = engine.split("/")

            if len(engine_components) < 2:
                raise ValueError(f"Invalid engine: {engine}")

            major_version = engine_components[1].split(".")[0]

            if database.version.split(".")[0] != major_version:
                params["version"] = major_version

        # The `updates` field is returned with an additional `pending` key that isn't
        # defined by the user, so we need to inject the actual value here.
        if params.get("updates") is not None:
            params["updates"]["pending"] = database.updates.pending

        # We want to explicitly include keys that are nullable in the update request
        # only if their corresponding "detach" parameter is True.
        nullable_keys = set()

        if self.module.params.get("detach_private_network"):
            nullable_keys.add("private_network")

        updated_fields = handle_updates(
            database,
            params,
            {
                "label",
                "allow_list",
                "cluster_size",
                "engine_config",
                "private_network",
                "updates",
                "type",
                "version",
            },
            self.register_action,
            nullable_keys=nullable_keys,
        )

        # NOTE: We don't poll for the database_update event here because it is not
        # triggered under all conditions.
        if len(updated_fields) > 0:
            wait_for_database_status(
                self.client,
                database,
                "active",
                timeout=self._timeout_ctx.seconds_remaining,
            )

        # Sometimes the cluster_size attribute doesn't update until shortly after
        # a resize operation
        if "cluster_size" in updated_fields:

            def __poll_condition() -> bool:
                database._api_get()
                return database.cluster_size == params["cluster_size"]

            poll_condition(
                __poll_condition,
                timeout=self._timeout_ctx.seconds_remaining,
                step=1,
            )

    def _populate_results(self, database: ValkeyDatabase) -> None:
        database._api_get()

        self.results["database"] = database._raw_json
        self.results["credentials"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.credentials)
        )
        self.results["ssl_cert"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.ssl)
        )

    def _handle_present(self) -> None:
        params = self.module.params

        result = safe_find(
            self.client.database.valkey_instances,
            ValkeyDatabase.label == params.get("label"),
        )
        if result is None:
            result = self._create()
            self.register_action(
                "Created Valkey database {0}".format(result.id)
            )

        self._update(result)

        self._populate_results(result)

    def _handle_else(self, state: str) -> None:
        params = self.module.params

        database = safe_find(
            self.client.database.valkey_instances,
            ValkeyDatabase.label == params.get("label"),
        )

        if database is not None:
            self._populate_results(database)

            if state == "suspend":
                self._handle_suspend(database)
            elif state == "resume":
                self._handle_resume(database)
            else:
                self._handle_absent(database)

    def _handle_absent(self, database: ValkeyDatabase) -> None:
        database.delete()
        self.register_action(f"Deleted Valkey database {database.id}")

    def _handle_suspend(self, database: ValkeyDatabase) -> None:
        database.suspend()
        self.register_action(f"Suspended Valkey database {database.id}")

    def _handle_resume(self, database: ValkeyDatabase) -> None:
        database.resume()
        self.register_action(f"Resumed Valkey database {database.id}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token module"""
        state = kwargs.get("state")

        if state == "present":
            self._handle_present()
        else:
            self._handle_else(state)

        return self.results


def main() -> None:
    """Constructs and calls the Linode Valkey database module"""
    Module()


if __name__ == "__main__":
    main()
