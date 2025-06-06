"""Documentation fragments for the database_mysql module"""

specdoc_examples = ['''
- name: Get all available engine configuration fields for MySQL databases
  linode.cloud.database_config_info:
    engine: mysql''', '''
- name: Get all available engine configuration fields for PostgreSQL databases
  linode.cloud.database_config_info:
    engine: postgresql''']

result_config_samples = [r'''
{
  "binlog_retention_period": {
    "description": "The minimum amount of time in seconds to keep binlog entries before deletion. This may be extended for services that require binlog entries for longer than the default for example if using the MySQL Debezium Kafka connector.",
    "example": 600,
    "maximum": 86400,
    "minimum": 600,
    "requires_restart": false,
    "type": "integer"
  },
  "mysql": {
    "connect_timeout": {
      "description": "The number of seconds that the mysqld server waits for a connect packet before responding with Bad handshake",
      "example": 10,
      "maximum": 3600,
      "minimum": 2,
      "requires_restart": false,
      "type": "integer"
    },
    "default_time_zone": {
      "description": "Default server time zone as an offset from UTC (from -12:00 to +12:00), a time zone name, or 'SYSTEM' to use the MySQL server default.",
      "example": "+03:00",
      "maxLength": 100,
      "minLength": 2,
      "pattern": "^([-+][\\d:]*|[\\w/]*)$",
      "requires_restart": false,
      "type": "string"
    },
    "group_concat_max_len": {
      "description": "The maximum permitted result length in bytes for the GROUP_CONCAT() function.",
      "example": 1024,
      "maximum": 18446744073709551615,
      "minimum": 4,
      "requires_restart": false,
      "type": "integer"
    },
    "information_schema_stats_expiry": {
      "description": "The time, in seconds, before cached statistics expire",
      "example": 86400,
      "maximum": 31536000,
      "minimum": 900,
      "requires_restart": false,
      "type": "integer"
    },
    "innodb_change_buffer_max_size": {
      "description": "Maximum size for the InnoDB change buffer, as a percentage of the total size of the buffer pool. Default is 25",
      "example": 30,
      "maximum": 50,
      "minimum": 0,
      "requires_restart": false,
      "type": "integer"
    },
    "innodb_flush_neighbors": {
      "description": "Specifies whether flushing a page from the InnoDB buffer pool also flushes other dirty pages in the same extent (default is 1): 0 - dirty pages in the same extent are not flushed, 1 - flush contiguous dirty pages in the same extent, 2 - flush dirty pages in the same extent",
      "example": 0,
      "maximum": 2,
      "minimum": 0,
      "requires_restart": false,
      "type": "integer"
    },
    "innodb_ft_min_token_size": {
      "description": "Minimum length of words that are stored in an InnoDB FULLTEXT index. Changing this parameter will lead to a restart of the MySQL service.",
      "example": 3,
      "maximum": 16,
      "minimum": 0,
      "requires_restart": true,
      "type": "integer"
    },
    "innodb_ft_server_stopword_table": {
      "description": "This option is used to specify your own InnoDB FULLTEXT index stopword list for all InnoDB tables.",
      "example": "db_name/table_name",
      "maxLength": 1024,
      "pattern": "^.+/.+$",
      "requires_restart": false,
      "type": [
        "null",
        "string"
      ]
    },
    "innodb_lock_wait_timeout": {
      "description": "The length of time in seconds an InnoDB transaction waits for a row lock before giving up. Default is 120.",
      "example": 50,
      "maximum": 3600,
      "minimum": 1,
      "requires_restart": false,
      "type": "integer"
    },
    "innodb_log_buffer_size": {
      "description": "The size in bytes of the buffer that InnoDB uses to write to the log files on disk.",
      "example": 16777216,
      "maximum": 4294967295,
      "minimum": 1048576,
      "requires_restart": false,
      "type": "integer"
    },
    "innodb_online_alter_log_max_size": {
      "description": "The upper limit in bytes on the size of the temporary log files used during online DDL operations for InnoDB tables.",
      "example": 134217728,
      "maximum": 1099511627776,
      "minimum": 65536,
      "requires_restart": false,
      "type": "integer"
    },
    "innodb_read_io_threads": {
      "description": "The number of I/O threads for read operations in InnoDB. Default is 4. Changing this parameter will lead to a restart of the MySQL service.",
      "example": 10,
      "maximum": 64,
      "minimum": 1,
      "requires_restart": true,
      "type": "integer"
    },
    "innodb_rollback_on_timeout": {
      "description": "When enabled a transaction timeout causes InnoDB to abort and roll back the entire transaction. Changing this parameter will lead to a restart of the MySQL service.",
      "example": true,
      "requires_restart": true,
      "type": "boolean"
    },
    "innodb_thread_concurrency": {
      "description": "Defines the maximum number of threads permitted inside of InnoDB. Default is 0 (infinite concurrency - no limit)",
      "example": 10,
      "maximum": 1000,
      "minimum": 0,
      "requires_restart": false,
      "type": "integer"
    },
    "innodb_write_io_threads": {
      "description": "The number of I/O threads for write operations in InnoDB. Default is 4. Changing this parameter will lead to a restart of the MySQL service.",
      "example": 10,
      "maximum": 64,
      "minimum": 1,
      "requires_restart": true,
      "type": "integer"
    },
    "interactive_timeout": {
      "description": "The number of seconds the server waits for activity on an interactive connection before closing it.",
      "example": 3600,
      "maximum": 604800,
      "minimum": 30,
      "requires_restart": false,
      "type": "integer"
    },
    "internal_tmp_mem_storage_engine": {
      "description": "The storage engine for in-memory internal temporary tables.",
      "enum": [
        "TempTable",
        "MEMORY"
      ],
      "example": "TempTable",
      "requires_restart": false,
      "type": "string"
    },
    "max_allowed_packet": {
      "description": "Size of the largest message in bytes that can be received by the server. Default is 67108864 (64M)",
      "example": 67108864,
      "maximum": 1073741824,
      "minimum": 102400,
      "requires_restart": false,
      "type": "integer"
    },
    "max_heap_table_size": {
      "description": "Limits the size of internal in-memory tables. Also set tmp_table_size. Default is 16777216 (16M)",
      "example": 16777216,
      "maximum": 1073741824,
      "minimum": 1048576,
      "requires_restart": false,
      "type": "integer"
    },
    "net_buffer_length": {
      "description": "Start sizes of connection buffer and result buffer. Default is 16384 (16K). Changing this parameter will lead to a restart of the MySQL service.",
      "example": 16384,
      "maximum": 1048576,
      "minimum": 1024,
      "requires_restart": true,
      "type": "integer"
    },
    "net_read_timeout": {
      "description": "The number of seconds to wait for more data from a connection before aborting the read.",
      "example": 30,
      "maximum": 3600,
      "minimum": 1,
      "requires_restart": false,
      "type": "integer"
    },
    "net_write_timeout": {
      "description": "The number of seconds to wait for a block to be written to a connection before aborting the write.",
      "example": 30,
      "maximum": 3600,
      "minimum": 1,
      "requires_restart": false,
      "type": "integer"
    },
    "sort_buffer_size": {
      "description": "Sort buffer size in bytes for ORDER BY optimization. Default is 262144 (256K)",
      "example": 262144,
      "maximum": 1073741824,
      "minimum": 32768,
      "requires_restart": false,
      "type": "integer"
    },
    "sql_mode": {
      "description": "Global SQL mode. Set to empty to use MySQL server defaults. When creating a new service and not setting this field Akamai default SQL mode (strict, SQL standard compliant) will be assigned.",
      "example": "ANSI,TRADITIONAL",
      "maxLength": 1024,
      "pattern": "^[A-Z_]*(,[A-Z_]+)*$",
      "requires_restart": false,
      "type": "string"
    },
    "sql_require_primary_key": {
      "description": "Require primary key to be defined for new tables or old tables modified with ALTER TABLE and fail if missing. It is recommended to always have primary keys because various functionality may break if any large table is missing them.",
      "example": true,
      "requires_restart": false,
      "type": "boolean"
    },
    "tmp_table_size": {
      "description": "Limits the size of internal in-memory tables. Also set max_heap_table_size. Default is 16777216 (16M)",
      "example": 16777216,
      "maximum": 1073741824,
      "minimum": 1048576,
      "requires_restart": false,
      "type": "integer"
    },
    "wait_timeout": {
      "description": "The number of seconds the server waits for activity on a noninteractive connection before closing it.",
      "example": 28800,
      "maximum": 2147483,
      "minimum": 1,
      "requires_restart": false,
      "type": "integer"
    }
  }
}''']
