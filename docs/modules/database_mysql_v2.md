# database_mysql_v2

Create, read, and update a Linode MySQL database.

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
- name: Create a basic MySQL database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    allow_list:
      - 0.0.0.0/0
    state: present
```

```yaml
- name: Create a MySQL database with three nodes
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-standard-1
    cluster_size: 3
    allow_list:
      - 0.0.0.0/0
    state: present
```

```yaml
- name: Create a MySQL database with an explicit maintenance schedule and engine configuration
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    engine_config:
        binlog_retention_period: 600
        mysql:
            connect_timeout: 20
    updates:
        duration: 4
        frequency: weekly
        hour_of_day: 16
        day_of_week: 4
    state: present
```

```yaml
- name: Create a MySQL database forked from another database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    fork:
        source: 12345
    state: present
```

```yaml
- name: Delete a MySQL database
  linode.cloud.database_mysql_v2:
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
| [`mysql` (sub-options)](#mysql) | <center>`dict`</center> | <center>Optional</center> | MySQL specific configuration fields.   |
| `binlog_retention_period` | <center>`int`</center> | <center>Optional</center> | The minimum amount of time in seconds to keep binlog entries before deletion. This may be extended for use cases like MySQL Debezium Kafka connector.   |

### mysql

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `connect_timeout` | <center>`int`</center> | <center>Optional</center> | The number of seconds that the mysqld server waits for a connect packet before responding with Bad handshake.   |
| `default_time_zone` | <center>`str`</center> | <center>Optional</center> | Default server time zone as an offset from UTC (from -12:00 to +12:00), a time zone name, or 'SYSTEM' to use the MySQL server default.   |
| `group_concat_max_len` | <center>`int`</center> | <center>Optional</center> | The maximum permitted result length in bytes for the GROUP_CONCAT() function.   |
| `information_schema_stats_expiry` | <center>`int`</center> | <center>Optional</center> | The time, in seconds, before cached statistics expire.   |
| `innodb_change_buffer_max_size` | <center>`int`</center> | <center>Optional</center> | Maximum size for the InnoDB change buffer, as a percentage of the total size of the buffer pool.   |
| `innodb_flush_neighbors` | <center>`int`</center> | <center>Optional</center> | Specifies whether flushing a page from the InnoDB buffer pool also flushes other dirty pages in the same extent.   |
| `innodb_ft_min_token_size` | <center>`int`</center> | <center>Optional</center> | Minimum length of words that are stored in an InnoDB FULLTEXT index.   |
| `innodb_ft_server_stopword_table` | <center>`str`</center> | <center>Optional</center> | This option is used to specify your own InnoDB FULLTEXT index stopword list for all InnoDB tables.   |
| `innodb_lock_wait_timeout` | <center>`int`</center> | <center>Optional</center> | The length of time in seconds an InnoDB transaction waits for a row lock before giving up.   |
| `innodb_log_buffer_size` | <center>`int`</center> | <center>Optional</center> | The size in bytes of the buffer that InnoDB uses to write to the log files on disk.   |
| `innodb_online_alter_log_max_size` | <center>`int`</center> | <center>Optional</center> | The upper limit in bytes on the size of the temporary log files used during online DDL operations for InnoDB tables.   |
| `innodb_read_io_threads` | <center>`int`</center> | <center>Optional</center> | The number of I/O threads for read operations in InnoDB.   |
| `innodb_rollback_on_timeout` | <center>`bool`</center> | <center>Optional</center> | When enabled a transaction timeout causes InnoDB to abort and roll back the entire transaction.   |
| `innodb_thread_concurrency` | <center>`int`</center> | <center>Optional</center> | Defines the maximum number of threads permitted inside of InnoDB.   |
| `innodb_write_io_threads` | <center>`int`</center> | <center>Optional</center> | The number of I/O threads for write operations in InnoDB.   |
| `interactive_timeout` | <center>`int`</center> | <center>Optional</center> | The number of seconds the server waits for activity on an interactive connection before closing it.   |
| `internal_tmp_mem_storage_engine` | <center>`str`</center> | <center>Optional</center> | The storage engine for in-memory internal temporary tables.  **(Choices: `TempTable`, `MEMORY`)** |
| `max_allowed_packet` | <center>`int`</center> | <center>Optional</center> | Size of the largest message in bytes that can be received by the server. Default is 67108864 (64M).   |
| `max_heap_table_size` | <center>`int`</center> | <center>Optional</center> | Limits the size of internal in-memory tables. Also set tmp_table_size. Default is 16777216 (16M).   |
| `net_buffer_length` | <center>`int`</center> | <center>Optional</center> | Start sizes of connection buffer and result buffer. Default is 16384 (16K).   |
| `net_read_timeout` | <center>`int`</center> | <center>Optional</center> | The number of seconds to wait for more data from a connection before aborting the read.   |
| `net_write_timeout` | <center>`int`</center> | <center>Optional</center> | The number of seconds to wait for a block to be written to a connection before aborting the write.   |
| `sort_buffer_size` | <center>`int`</center> | <center>Optional</center> | Sort buffer size in bytes for ORDER BY optimization. Default is 262144 (256K).   |
| `sql_mode` | <center>`str`</center> | <center>Optional</center> | Global SQL mode. Set to empty to use MySQL server defaults.   |
| `sql_require_primary_key` | <center>`bool`</center> | <center>Optional</center> | Require primary key to be defined for new tables or old tables modified with ALTER TABLE and fail if missing.   |
| `tmp_table_size` | <center>`int`</center> | <center>Optional</center> | Limits the size of internal in-memory tables. Also sets max_heap_table_size. Default is 16777216 (16M).   |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The number of seconds the server waits for activity on a noninteractive connection before closing it.   |

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
          "engine": "mysql",
          "engine_config": {
            "binlog_retention_period": 600,
            "mysql": {
              "connect_timeout": 20
            }
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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-mysql-instance) for a list of returned fields


- `ssl_cert` - The SSL CA certificate for an accessible Managed MySQL Database.

    - Sample Response:
        ```json
        {
          "ca_certificate": "LS0tLS1CRUdJ...=="
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-mysql-instance-ssl) for a list of returned fields


- `credentials` - The root username and password for an accessible Managed MySQL Database.

    - Sample Response:
        ```json
        {
          "password": "s3cur3P@ssw0rd",
          "username": "akmadmin"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-mysql-instance-credentials) for a list of returned fields


