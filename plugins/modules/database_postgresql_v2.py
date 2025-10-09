#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the implementation for the linode.cloud.database_postgresql_v2 module."""

from __future__ import absolute_import, division, print_function

import copy
from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_postgresql_v2 as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import (
    SPEC_FORK,
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
from linode_api4 import PostgreSQLDatabase

SPEC_ENGINE_CONFIG_PG = {
    "autovacuum_analyze_scale_factor": SpecField(
        type=FieldType.float,
        description=[
            "Specifies a fraction of the table size to add to "
            + "autovacuum_analyze_threshold when deciding "
            + "whether to trigger an ANALYZE.",
            "The default is 0.2 (20% of table size).",
        ],
    ),
    "autovacuum_analyze_threshold": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the minimum number of inserted, updated or deleted "
            + "tuples needed to trigger "
            "an ANALYZE in any one table.",
            "The default is 50 tuples.",
        ],
    ),
    "autovacuum_max_workers": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the maximum number of autovacuum processes "
            + "(other than the autovacuum launcher) "
            + "that may be running at any one time.",
            "The default is three.",
            "This parameter can only be set at server start.",
        ],
    ),
    "autovacuum_naptime": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the minimum delay between autovacuum runs on any given database.",
            "The delay is measured in seconds, and the default is one minute.",
        ],
    ),
    "autovacuum_vacuum_cost_delay": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the cost delay value that will be used in automatic VACUUM operations.",
            "If -1 is specified, the regular vacuum_cost_delay value will be used.",
            "The default value is 20 milliseconds.",
        ],
    ),
    "autovacuum_vacuum_cost_limit": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the cost limit value that will be used in automatic VACUUM operations.",
            "If -1 is specified (which is the default), the regular "
            + "vacuum_cost_limit value will be used.",
        ],
    ),
    "autovacuum_vacuum_scale_factor": SpecField(
        type=FieldType.float,
        description=[
            "Specifies a fraction of the table size to add to "
            + "autovacuum_vacuum_threshold when deciding "
            + "whether to trigger a VACUUM.",
            "The default is 0.2 (20% of table size).",
        ],
    ),
    "autovacuum_vacuum_threshold": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the minimum number of updated or deleted tuples needed to "
            + "trigger a VACUUM in any one table.",
            "The default is 50 tuples.",
        ],
    ),
    "bgwriter_delay": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the delay between activity rounds for the "
            + "background writer in milliseconds.",
            "Default is 200.",
        ],
    ),
    "bgwriter_flush_after": SpecField(
        type=FieldType.integer,
        description=[
            "Whenever more than bgwriter_flush_after bytes have been "
            + "written by the background writer, attempt to "
            + "force the OS to issue these writes to the underlying storage.",
            "Specified in kilobytes, default is 512.",
            "Setting of 0 disables forced writeback.",
        ],
    ),
    "bgwriter_lru_maxpages": SpecField(
        type=FieldType.integer,
        description=[
            "In each round, no more than this many buffers will be "
            + "written by the background writer.",
            "Setting this to zero disables background writing.",
            "Default is 100.",
        ],
    ),
    "bgwriter_lru_multiplier": SpecField(
        type=FieldType.float,
        description=[
            "The average recent need for new buffers is multiplied by "
            + "bgwriter_lru_multiplier to arrive at an estimate of the number "
            + "that will be needed during the next round, (up to bgwriter_lru_maxpages).",
            "1.0 represents a “just in time” policy of writing exactly the number of "
            + "buffers predicted to be needed.",
            "Larger values provide some cushion against spikes in demand, "
            + "while smaller values intentionally leave writes "
            "to be done by server processes.",
            "The default is 2.0.",
        ],
    ),
    "deadlock_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "This is the amount of time, in milliseconds, to wait on a lock "
            + "before checking to see if there is a deadlock condition."
        ],
    ),
    "default_toast_compression": SpecField(
        type=FieldType.string,
        description=[
            "Specifies the default TOAST compression method for values of "
            + "compressible columns (the default is lz4)."
        ],
        choices=["pglz", "lz4"],
    ),
    "idle_in_transaction_session_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "Time out sessions with open transactions after this number of milliseconds."
        ],
    ),
    "jit": SpecField(
        type=FieldType.bool,
        description=[
            "Controls system-wide use of Just-in-Time Compilation (JIT)."
        ],
    ),
    "max_files_per_process": SpecField(
        type=FieldType.integer,
        description=[
            "PostgreSQL maximum number of files that can be open per process."
        ],
    ),
    "max_locks_per_transaction": SpecField(
        type=FieldType.integer,
        description=["PostgreSQL maximum locks per transaction."],
    ),
    "max_logical_replication_workers": SpecField(
        type=FieldType.integer,
        description=[
            "PostgreSQL maximum logical replication workers "
            + "(taken from the pool of max_parallel_workers)."
        ],
    ),
    "max_parallel_workers": SpecField(
        type=FieldType.integer,
        description=[
            "Sets the maximum number of workers that the system "
            + "can support for parallel queries."
        ],
    ),
    "max_parallel_workers_per_gather": SpecField(
        type=FieldType.integer,
        description=[
            "Sets the maximum number of workers that can be started "
            + "by a single Gather or Gather Merge node."
        ],
    ),
    "max_pred_locks_per_transaction": SpecField(
        type=FieldType.integer,
        description=["PostgreSQL maximum predicate locks per transaction."],
    ),
    "max_replication_slots": SpecField(
        type=FieldType.integer,
        description=["PostgreSQL maximum replication slots."],
    ),
    "max_slot_wal_keep_size": SpecField(
        type=FieldType.integer,
        description=[
            "PostgreSQL maximum WAL size (MB) reserved for replication slots.",
            "Default is -1 (unlimited).",
            "wal_keep_size minimum WAL size setting takes precedence over this.",
        ],
    ),
    "max_stack_depth": SpecField(
        type=FieldType.integer,
        description=["Maximum depth of the stack in bytes."],
    ),
    "max_standby_archive_delay": SpecField(
        type=FieldType.integer,
        description=["Max standby archive delay in milliseconds."],
    ),
    "max_standby_streaming_delay": SpecField(
        type=FieldType.integer,
        description=["Max standby streaming delay in milliseconds."],
    ),
    "max_wal_senders": SpecField(
        type=FieldType.integer,
        description=["PostgreSQL maximum WAL senders."],
    ),
    "max_worker_processes": SpecField(
        type=FieldType.integer,
        description=[
            "Sets the maximum number of background processes that the system can support."
        ],
    ),
    "password_encryption": SpecField(
        type=FieldType.string,
        description=["Chooses the algorithm for encrypting passwords."],
        choices=["md5", "scram-sha-256"],
    ),
    "pg_partman_bgw.interval": SpecField(
        type=FieldType.integer,
        description=[
            "Sets the time interval to run pg_partman's scheduled tasks."
        ],
    ),
    "pg_partman_bgw.role": SpecField(
        type=FieldType.string,
        description=[
            "Controls which role to use for pg_partman's scheduled background tasks."
        ],
    ),
    "pg_stat_monitor.pgsm_enable_query_plan": SpecField(
        type=FieldType.bool,
        description=["Enables or disables query plan monitoring."],
    ),
    "pg_stat_monitor.pgsm_max_buckets": SpecField(
        type=FieldType.integer,
        description=["Sets the maximum number of buckets."],
    ),
    "pg_stat_statements.track": SpecField(
        type=FieldType.string,
        description=[
            "Controls which statements are counted.",
            "Specify 'top' to track top-level statements (those issued directly by clients), "
            + "'all' to also track nested statements (such as statements "
            + "invoked within functions), or 'none' to disable statement statistics collection.",
            "The default value is 'top'.",
        ],
        choices=["top", "all", "none"],
    ),
    "temp_file_limit": SpecField(
        type=FieldType.integer,
        description=[
            "PostgreSQL temporary file limit in KiB, -1 for unlimited."
        ],
    ),
    "timezone": SpecField(
        type=FieldType.string,
        description=["PostgreSQL service timezone."],
    ),
    "track_activity_query_size": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies the number of bytes reserved to track the currently "
            + "executing command for each active session."
        ],
    ),
    "track_commit_timestamp": SpecField(
        type=FieldType.string,
        description=["Record commit time of transactions."],
        choices=["on", "off"],
    ),
    "track_functions": SpecField(
        type=FieldType.string,
        description=["Enables tracking of function call counts and time used."],
        choices=["none", "pl", "all"],
    ),
    "track_io_timing": SpecField(
        type=FieldType.string,
        description=[
            "Enables timing of database I/O calls.",
            "This parameter is off by default, because it will repeatedly "
            + "query the operating system for the current time, which may "
            "cause significant overhead on some platforms.",
        ],
    ),
    "wal_sender_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "Terminate replication connections that are inactive for "
            + "longer than this amount of time, in milliseconds.",
            "Setting this value to zero disables the timeout.",
        ],
    ),
    "wal_writer_delay": SpecField(
        type=FieldType.integer,
        description=[
            "WAL flush interval in milliseconds.",
            "Note that setting this value to lower than the default 200ms "
            + "may negatively impact performance.",
        ],
    ),
}

SPEC_ENGINE_CONFIG_PGLOOKOUT = {
    "max_failover_replication_time_lag": SpecField(
        type=FieldType.integer,
        description=[
            "Number of seconds of master unavailability before "
            + "triggering database failover to standby."
        ],
    )
}

SPEC_ENGINE_CONFIG = {
    "pg": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_ENGINE_CONFIG_PG,
        description=[
            "The configuration for PostgreSQL.",
            "Contains settings and controls for database behavior.",
        ],
    ),
    "pglookout": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_ENGINE_CONFIG_PGLOOKOUT,
        description=[
            "The configuration for pglookout.",
            "Contains controls for failover and replication settings.",
        ],
    ),
    "pg_stat_monitor_enable": SpecField(
        type=FieldType.bool,
        description=[
            "Enable the pg_stat_monitor extension.",
            "Enabling this extension will cause the cluster to be restarted.",
            "When this extension is enabled, pg_stat_statements results "
            + "for utility commands are unreliable.",
        ],
    ),
    "shared_buffers_percentage": SpecField(
        type=FieldType.float,
        description=[
            "Percentage of total RAM that the database server uses for shared memory buffers.",
            "Valid range is 20-60 (float), which corresponds to 20% - 60%.",
            "This setting adjusts the shared_buffers configuration value.",
        ],
    ),
    "work_mem": SpecField(
        type=FieldType.integer,
        description=[
            "Sets the maximum amount of memory to be used by a "
            + "query operation (such as a sort or hash table) "
            + "before writing to temporary disk files, in MB.",
            "Default is 1MB + 0.075% of total RAM (up to 32MB).",
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
            "The Linode Instance type used by the Managed Database for its nodes."
        ],
        editable=True,
    ),
    "fork": SpecField(
        type=FieldType.dict,
        description=["Information about a database to fork from."],
        suboptions=SPEC_FORK,
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
        "Create, read, and update a Linode PostgreSQL database.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "database": SpecReturnValue(
            description="The database in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-postgre-sql-instance",
            type=FieldType.dict,
            sample=docs.result_database_samples,
        ),
        "ssl_cert": SpecReturnValue(
            description="The SSL CA certificate for an accessible Managed PostgreSQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-postgresql-instance-ssl",
            type=FieldType.dict,
            sample=docs.result_ssl_cert_samples,
        ),
        "credentials": SpecReturnValue(
            description="The root username and password for an "
            "accessible Managed PostgreSQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-postgre-sql-instance-credentials",
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
    """Module implementation for database_postgresql_v2."""

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

    def _create(self) -> PostgreSQLDatabase:
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

        # This is necessary because `type` is a Python-reserved keyword
        if "type" in params:
            params["ltype"] = params.pop("type")

        create_poller = self.client.polling.event_poller_create(
            "database", "database_create"
        )

        database = self.client.database.postgresql_create(**params)

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
        updates = params.get("updates")
        if updates is not None:
            database.updates = params.get("updates")
            database.save()

            wait_for_database_status(
                self.client,
                database,
                "active",
                timeout=self._timeout_ctx.seconds_remaining,
            )

        return database

    def _update(self, database: PostgreSQLDatabase) -> None:
        database._api_get()

        params = copy.deepcopy(self.module.params)

        # The database PUT endpoint accepts `version` rather than `engine`
        engine = params.pop("engine", None)
        if engine is not None:
            engine_components = engine.split("/")

            if len(engine_components) < 2:
                raise ValueError(f"Invalid engine: {engine}")

            major_version = int(engine_components[1])

            if int(database.version.split(".")[0]) != major_version:
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

    def _populate_results(self, database: PostgreSQLDatabase) -> None:
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
            self.client.database.postgresql_instances,
            PostgreSQLDatabase.label == params.get("label"),
        )
        if result is None:
            result = self._create()
            self.register_action(
                "Created PostgreSQL database {0}".format(result.id)
            )

        self._update(result)

        self._populate_results(result)

    def _handle_else(self, state: str) -> None:
        params = self.module.params

        database = safe_find(
            self.client.database.postgresql_instances,
            PostgreSQLDatabase.label == params.get("label"),
        )

        if database is not None:
            self._populate_results(database)

            if state == "suspend":
                self._handle_suspend(database)
            elif state == "resume":
                self._handle_resume(database)
            else:
                self._handle_absent(database)

    def _handle_absent(self, database: PostgreSQLDatabase) -> None:
        database.delete()
        self.register_action(f"Deleted PostgreSQL database {database.id}")

    def _handle_suspend(self, database: PostgreSQLDatabase) -> None:
        database.suspend()
        self.register_action(f"Suspended PostgreSQL database {database.id}")

    def _handle_resume(self, database: PostgreSQLDatabase) -> None:
        database.resume()
        self.register_action(f"Resumed PostgreSQL database {database.id}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token module"""
        state = kwargs.get("state")

        if state == "present":
            self._handle_present()
        else:
            self._handle_else(state)

        return self.results


def main() -> None:
    """Constructs and calls the Linode PostgreSQL database module"""
    Module()


if __name__ == "__main__":
    main()
