# database_postgresql_v2

Create, read, and update a Linode PostgreSQL database.

- [Minimum Required Fields](#minimum-required-fields)
- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Minimum Required Fields
| Field       | Type  | Required     | Description                                                                                                                                                                                                              |
|-------------|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api_token` | `str` | **Required** | The Linode account personal access token. It is necessary to run the module. <br/>It can be exposed by the environment variable `LINODE_API_TOKEN` instead. <br/>See details in [Usage](https://github.com/linode/ansible_linode?tab=readme-ov-file#usage). |

## Examples

```yaml
- name: Create a basic PostgreSQL database
  linode.cloud.database_postgresql_v2:
    label: my-db
    region: us-mia
    engine: postgresql/16
    type: g6-nanode-1
    allow_list:
      - 0.0.0.0/0
    state: present
```

```yaml
- name: Create a PostgreSQL database with three nodes
  linode.cloud.database_postgresql_v2:
    label: my-db
    region: us-mia
    engine: postgresql/16
    type: g6-standard-1
    cluster_size: 3
    allow_list:
      - 0.0.0.0/0
    state: present
```

```yaml
- name: Create a PostgreSQL database with an explicit maintenance schedule and engine configuration
  linode.cloud.database_postgresql_v2:
    label: my-db
    region: us-mia
    engine: postgresql/16
    type: g6-nanode-1
    engine_config:
        work_mem: 1023
        pg:
            autovacuum_analyze_scale_factor: 0.2
    updates:
        duration: 4
        frequency: weekly
        hour_of_day: 16
        day_of_week: 4
    state: present
```

```yaml
- name: Create a PostgreSQL database forked from another database
  linode.cloud.database_postgresql_v2:
    label: my-db
    region: us-mia
    engine: postgresql/16
    type: g6-nanode-1
    fork:
        source: 12345
    state: present
```

```yaml
- name: Delete a PostgreSQL database
  linode.cloud.database_postgresql_v2:
    label: my-db
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the Managed Database.  **(Choices: `resume`, `suspend`, `present`, `absent`)** |
| `allow_list` | <center>`list`</center> | <center>Optional</center> | A list of IP addresses and CIDR ranges that can access the Managed Database.  **(Updatable)** |
| `cluster_size` | <center>`int`</center> | <center>Optional</center> | The number of Linode instance nodes deployed to the Managed Database.  **(Updatable)** |
| `engine` | <center>`str`</center> | <center>Optional</center> | The Managed Database engine in engine/version format.  **(Updatable)** |
| [`engine_config` (sub-options)](#engine_config) | <center>`dict`</center> | <center>Optional</center> | Various parameters used to configure this database's underlying engine. NOTE: If a configuration parameter is not current accepted by this field, configure using the linode.cloud.api_request module.  **(Updatable)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Managed Database.   |
| `region` | <center>`str`</center> | <center>Optional</center> | The region of the Managed Database.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The Linode Instance type used by the Managed Database for its nodes.  **(Updatable)** |
| [`fork` (sub-options)](#fork) | <center>`dict`</center> | <center>Optional</center> | Information about a database to fork from.   |
| [`updates` (sub-options)](#updates) | <center>`dict`</center> | <center>Optional</center> | Configuration settings for automated patch update maintenance for the Managed Database.  **(Updatable)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The maximum number of seconds a poll operation can take before raising an error.  **(Default: `2700`)** |

### engine_config

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`pg` (sub-options)](#pg) | <center>`dict`</center> | <center>Optional</center> | The configuration for PostgreSQL. Contains settings and controls for database behavior.   |
| [`pglookout` (sub-options)](#pglookout) | <center>`dict`</center> | <center>Optional</center> | The configuration for pglookout. Contains controls for failover and replication settings.   |
| `pg_stat_monitor_enable` | <center>`bool`</center> | <center>Optional</center> | Enable the pg_stat_monitor extension. Enabling this extension will cause the cluster to be restarted. When this extension is enabled, pg_stat_statements results for utility commands are unreliable.   |
| `shared_buffers_percentage` | <center>`float`</center> | <center>Optional</center> | Percentage of total RAM that the database server uses for shared memory buffers. Valid range is 20-60 (float), which corresponds to 20% - 60%. This setting adjusts the shared_buffers configuration value.   |
| `work_mem` | <center>`int`</center> | <center>Optional</center> | Sets the maximum amount of memory to be used by a query operation (such as a sort or hash table) before writing to temporary disk files, in MB. Default is 1MB + 0.075% of total RAM (up to 32MB).   |

### pg

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `autovacuum_analyze_scale_factor` | <center>`float`</center> | <center>Optional</center> | Specifies a fraction of the table size to add to autovacuum_analyze_threshold when deciding whether to trigger an ANALYZE. The default is 0.2 (20% of table size).   |
| `autovacuum_analyze_threshold` | <center>`int`</center> | <center>Optional</center> | Specifies the minimum number of inserted, updated or deleted tuples needed to trigger an ANALYZE in any one table. The default is 50 tuples.   |
| `autovacuum_max_workers` | <center>`int`</center> | <center>Optional</center> | Specifies the maximum number of autovacuum processes (other than the autovacuum launcher) that may be running at any one time. The default is three. This parameter can only be set at server start.   |
| `autovacuum_naptime` | <center>`int`</center> | <center>Optional</center> | Specifies the minimum delay between autovacuum runs on any given database. The delay is measured in seconds, and the default is one minute.   |
| `autovacuum_vacuum_cost_delay` | <center>`int`</center> | <center>Optional</center> | Specifies the cost delay value that will be used in automatic VACUUM operations. If -1 is specified, the regular vacuum_cost_delay value will be used. The default value is 20 milliseconds.   |
| `autovacuum_vacuum_cost_limit` | <center>`int`</center> | <center>Optional</center> | Specifies the cost limit value that will be used in automatic VACUUM operations. If -1 is specified (which is the default), the regular vacuum_cost_limit value will be used.   |
| `autovacuum_vacuum_scale_factor` | <center>`float`</center> | <center>Optional</center> | Specifies a fraction of the table size to add to autovacuum_vacuum_threshold when deciding whether to trigger a VACUUM. The default is 0.2 (20% of table size).   |
| `autovacuum_vacuum_threshold` | <center>`int`</center> | <center>Optional</center> | Specifies the minimum number of updated or deleted tuples needed to trigger a VACUUM in any one table. The default is 50 tuples.   |
| `bgwriter_delay` | <center>`int`</center> | <center>Optional</center> | Specifies the delay between activity rounds for the background writer in milliseconds. Default is 200.   |
| `bgwriter_flush_after` | <center>`int`</center> | <center>Optional</center> | Whenever more than bgwriter_flush_after bytes have been written by the background writer, attempt to force the OS to issue these writes to the underlying storage. Specified in kilobytes, default is 512. Setting of 0 disables forced writeback.   |
| `bgwriter_lru_maxpages` | <center>`int`</center> | <center>Optional</center> | In each round, no more than this many buffers will be written by the background writer. Setting this to zero disables background writing. Default is 100.   |
| `bgwriter_lru_multiplier` | <center>`float`</center> | <center>Optional</center> | The average recent need for new buffers is multiplied by bgwriter_lru_multiplier to arrive at an estimate of the number that will be needed during the next round, (up to bgwriter_lru_maxpages). 1.0 represents a “just in time” policy of writing exactly the number of buffers predicted to be needed. Larger values provide some cushion against spikes in demand, while smaller values intentionally leave writes to be done by server processes. The default is 2.0.   |
| `deadlock_timeout` | <center>`int`</center> | <center>Optional</center> | This is the amount of time, in milliseconds, to wait on a lock before checking to see if there is a deadlock condition.   |
| `default_toast_compression` | <center>`str`</center> | <center>Optional</center> | Specifies the default TOAST compression method for values of compressible columns (the default is lz4).  **(Choices: `pglz`, `lz4`)** |
| `idle_in_transaction_session_timeout` | <center>`int`</center> | <center>Optional</center> | Time out sessions with open transactions after this number of milliseconds.   |
| `jit` | <center>`bool`</center> | <center>Optional</center> | Controls system-wide use of Just-in-Time Compilation (JIT).   |
| `max_files_per_process` | <center>`int`</center> | <center>Optional</center> | PostgreSQL maximum number of files that can be open per process.   |
| `max_locks_per_transaction` | <center>`int`</center> | <center>Optional</center> | PostgreSQL maximum locks per transaction.   |
| `max_logical_replication_workers` | <center>`int`</center> | <center>Optional</center> | PostgreSQL maximum logical replication workers (taken from the pool of max_parallel_workers).   |
| `max_parallel_workers` | <center>`int`</center> | <center>Optional</center> | Sets the maximum number of workers that the system can support for parallel queries.   |
| `max_parallel_workers_per_gather` | <center>`int`</center> | <center>Optional</center> | Sets the maximum number of workers that can be started by a single Gather or Gather Merge node.   |
| `max_pred_locks_per_transaction` | <center>`int`</center> | <center>Optional</center> | PostgreSQL maximum predicate locks per transaction.   |
| `max_replication_slots` | <center>`int`</center> | <center>Optional</center> | PostgreSQL maximum replication slots.   |
| `max_slot_wal_keep_size` | <center>`int`</center> | <center>Optional</center> | PostgreSQL maximum WAL size (MB) reserved for replication slots. Default is -1 (unlimited). wal_keep_size minimum WAL size setting takes precedence over this.   |
| `max_stack_depth` | <center>`int`</center> | <center>Optional</center> | Maximum depth of the stack in bytes.   |
| `max_standby_archive_delay` | <center>`int`</center> | <center>Optional</center> | Max standby archive delay in milliseconds.   |
| `max_standby_streaming_delay` | <center>`int`</center> | <center>Optional</center> | Max standby streaming delay in milliseconds.   |
| `max_wal_senders` | <center>`int`</center> | <center>Optional</center> | PostgreSQL maximum WAL senders.   |
| `max_worker_processes` | <center>`int`</center> | <center>Optional</center> | Sets the maximum number of background processes that the system can support.   |
| `password_encryption` | <center>`str`</center> | <center>Optional</center> | Chooses the algorithm for encrypting passwords.  **(Choices: `md5`, `scram-sha-256`)** |
| `pg_partman_bgw.interval` | <center>`int`</center> | <center>Optional</center> | Sets the time interval to run pg_partman's scheduled tasks.   |
| `pg_partman_bgw.role` | <center>`str`</center> | <center>Optional</center> | Controls which role to use for pg_partman's scheduled background tasks.   |
| `pg_stat_monitor.pgsm_enable_query_plan` | <center>`bool`</center> | <center>Optional</center> | Enables or disables query plan monitoring.   |
| `pg_stat_monitor.pgsm_max_buckets` | <center>`int`</center> | <center>Optional</center> | Sets the maximum number of buckets.   |
| `pg_stat_statements.track` | <center>`str`</center> | <center>Optional</center> | Controls which statements are counted. Specify 'top' to track top-level statements (those issued directly by clients), 'all' to also track nested statements (such as statements invoked within functions), or 'none' to disable statement statistics collection. The default value is 'top'.  **(Choices: `top`, `all`, `none`)** |
| `temp_file_limit` | <center>`int`</center> | <center>Optional</center> | PostgreSQL temporary file limit in KiB, -1 for unlimited.   |
| `timezone` | <center>`str`</center> | <center>Optional</center> | PostgreSQL service timezone.   |
| `track_activity_query_size` | <center>`int`</center> | <center>Optional</center> | Specifies the number of bytes reserved to track the currently executing command for each active session.   |
| `track_commit_timestamp` | <center>`str`</center> | <center>Optional</center> | Record commit time of transactions.  **(Choices: `on`, `off`)** |
| `track_functions` | <center>`str`</center> | <center>Optional</center> | Enables tracking of function call counts and time used.  **(Choices: `none`, `pl`, `all`)** |
| `track_io_timing` | <center>`str`</center> | <center>Optional</center> | Enables timing of database I/O calls. This parameter is off by default, because it will repeatedly query the operating system for the current time, which may cause significant overhead on some platforms.   |
| `wal_sender_timeout` | <center>`int`</center> | <center>Optional</center> | Terminate replication connections that are inactive for longer than this amount of time, in milliseconds. Setting this value to zero disables the timeout.   |
| `wal_writer_delay` | <center>`int`</center> | <center>Optional</center> | WAL flush interval in milliseconds. Note that setting this value to lower than the default 200ms may negatively impact performance.   |

### pglookout

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `max_failover_replication_time_lag` | <center>`int`</center> | <center>Optional</center> | Number of seconds of master unavailability before triggering database failover to standby.   |

### fork

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `restore_time` | <center>`str`</center> | <center>Optional</center> | The database timestamp from which it was restored.   |
| `source` | <center>`int`</center> | <center>Optional</center> | The instance id of the database that was forked from.   |

### updates

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `day_of_week` | <center>`int`</center> | <center>**Required**</center> | The day to perform maintenance. 1=Monday, 2=Tuesday, etc.  **(Choices: `1`, `2`, `3`, `4`, `5`, `6`, `7`)** |
| `duration` | <center>`int`</center> | <center>**Required**</center> | The maximum maintenance window time in hours.   |
| `hour_of_day` | <center>`int`</center> | <center>**Required**</center> | The hour to begin maintenance based in UTC time.   |
| `frequency` | <center>`str`</center> | <center>Optional</center> | The frequency at which maintenance occurs.  **(Choices: `weekly`; Default: `weekly`)** |

## Return Values

- `database` - The database in JSON serialized form.

    - Sample Response:
        ```json
        {
          "allow_list": [
            "10.0.0.3/32"
          ],
          "cluster_size": 3,
          "created": "2025-02-10T20:10:20",
          "encrypted": true,
          "engine": "postgresql",
          "engine_config": {
            "pg": {
              "autovacuum_analyze_scale_factor": 0.2
            },
            "work_mem": 1023
          },
          "hosts": {
            "primary": "a225891-akamai-prod-1798333-default.g2a.akamaidb.net",
            "standby": "replica-a225891-akamai-prod-1798333-default.g2a.akamaidb.net"
          },
          "id": 12345,
          "label": "my-db",
          "members": {
            "172.104.207.136": "primary",
            "194.195.112.177": "failover",
            "45.79.126.72": "failover"
          },
          "oldest_restore_time": "2025-02-10T20:15:07",
          "platform": "rdbms-default",
          "port": 11876,
          "region": "ap-west",
          "ssl_connection": true,
          "status": "active",
          "total_disk_size_gb": 30,
          "type": "g6-standard-1",
          "updated": "2025-02-10T20:25:55",
          "updates": {
            "day_of_week": 4,
            "duration": 4,
            "frequency": "weekly",
            "hour_of_day": 16,
            "pending": []
          },
          "used_disk_size_gb": 0,
          "version": "8.0.35"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-postgre-sql-instance) for a list of returned fields


- `ssl_cert` - The SSL CA certificate for an accessible Managed PostgreSQL Database.

    - Sample Response:
        ```json
        {
          "ca_certificate": "LS0tLS1CRUdJ...=="
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-postgresql-instance-ssl) for a list of returned fields


- `credentials` - The root username and password for an accessible Managed PostgreSQL Database.

    - Sample Response:
        ```json
        {
          "password": "s3cur3P@ssw0rd",
          "username": "akmadmin"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-postgre-sql-instance-credentials) for a list of returned fields


