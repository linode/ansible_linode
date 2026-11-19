# database_valkey_v2

Create, read, and update a Linode Valkey database.

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
- name: Create a basic Valkey database
  linode.cloud.database_valkey_v2:
    label: my-db
    region: us-mia
    engine: valkey/8.1
    type: g6-dedicated-2
    allow_list:
      - 0.0.0.0/0
    state: present
```

```yaml
- name: Create a three-node Valkey database
  linode.cloud.database_valkey_v2:
    label: my-db
    region: us-mia
    engine: valkey/8.1
    type: g6-dedicated-4
    cluster_size: 3
    state: present
```

```yaml
- name: Create a Valkey database with maintenance and engine configuration
  linode.cloud.database_valkey_v2:
    label: my-db
    region: us-mia
    engine: valkey/8.1
    type: g6-dedicated-2
    engine_config:
      backup_hour: 3
      backup_minute: 30
      frequent_snapshots: true
      valkey_persistence: rdb
    updates:
      duration: 4
      frequency: weekly
      hour_of_day: 16
      day_of_week: 4
    state: present
```

```yaml
- name: Restore a Valkey database from an available snapshot
  linode.cloud.database_valkey_v2:
    label: my-restored-db
    region: us-mia
    engine: valkey/8.1
    type: g6-dedicated-2
    fork:
      source: 12345
      restore_time: "2026-10-05T14:00:00"
    state: present
```

```yaml
- name: Delete a Valkey database
  linode.cloud.database_valkey_v2:
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
| `detach_private_network` | <center>`bool`</center> | <center>Optional</center> | If true, the Managed Database will be detached from its current private network when `private_network` is null. If the Managed Database is not currently attached to a private network or the private_network field is specified, this option has no effect. This is not necessary when switching between VPC subnets.  **(Default: `False`)** |
| [`private_network` (sub-options)](#private_network) | <center>`dict`</center> | <center>Optional</center> | Restricts access to this database using a virtual private cloud (VPC) that you've configured in the region where the database will live.  **(Updatable)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The region of the Managed Database.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The Linode Instance type used by the Managed Database for its nodes. Must support Valkey; see GET /databases/types.  **(Updatable)** |
| [`fork` (sub-options)](#fork) | <center>`dict`</center> | <center>Optional</center> | Information about a Valkey database to fork from. restore_time must be one of the source database's available_restore_times values.   |
| [`updates` (sub-options)](#updates) | <center>`dict`</center> | <center>Optional</center> | Configuration settings for automated patch update maintenance for the Managed Database.  **(Updatable)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The maximum number of seconds a poll operation can take before raising an error.  **(Default: `2700`)** |

### engine_config

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `backup_hour` | <center>`int`</center> | <center>Optional</center> | The hour of day (UTC) when the backup starts.   |
| `backup_minute` | <center>`int`</center> | <center>Optional</center> | The minute of the hour when the backup starts.   |
| `frequent_snapshots` | <center>`bool`</center> | <center>Optional</center> | Enable frequent local RDB snapshots.   |
| `valkey_acl_channels_default` | <center>`str`</center> | <center>Optional</center> | The default ACL for pub/sub channels.  **(Choices: `allchannels`, `resetchannels`)** |
| `valkey_active_expire_effort` | <center>`int`</center> | <center>Optional</center> | The effort used to expire active keys.   |
| `valkey_activedefrag` | <center>`bool`</center> | <center>Optional</center> | Enable active memory defragmentation.   |
| `valkey_lfu_decay_time` | <center>`int`</center> | <center>Optional</center> | The LFU counter decay time.   |
| `valkey_lfu_log_factor` | <center>`int`</center> | <center>Optional</center> | The LFU counter logarithm factor.   |
| `valkey_maxmemory_policy` | <center>`str`</center> | <center>Optional</center> | The policy used when Valkey reaches maxmemory.  **(Choices: `noeviction`, `allkeys-lru`, `volatile-lru`, `allkeys-random`, `volatile-random`, `volatile-ttl`, `volatile-lfu`, `allkeys-lfu`)** |
| `valkey_number_of_databases` | <center>`int`</center> | <center>Optional</center> | The number of databases available in the Valkey instance.   |
| `valkey_persistence` | <center>`str`</center> | <center>Optional</center> | The Valkey persistence mode. When set to off, backup scheduling and maintenance updates are not supported.  **(Choices: `off`, `rdb`)** |
| `valkey_pubsub_client_output_buffer_limit` | <center>`int`</center> | <center>Optional</center> | The pub/sub client output buffer limit.   |
| `valkey_timeout` | <center>`int`</center> | <center>Optional</center> | The number of seconds before an idle client connection closes.   |

### private_network

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `vpc_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the virtual private cloud (VPC) to restrict access to this database using   |
| `subnet_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the VPC subnet to restrict access to this database using.   |
| `public_access` | <center>`bool`</center> | <center>Optional</center> | Set to `true` to allow clients outside of the VPC to connect to the database using a public IP address.  **(Default: `False`)** |

### fork

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `restore_time` | <center>`str`</center> | <center>**Required**</center> | The timestamp to restore from. Must be one of the source database's available_restore_times values.   |
| `source` | <center>`int`</center> | <center>**Required**</center> | The instance ID of the database to fork from.   |

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
          "available_restore_times": [
            "2026-10-05T14:00:00"
          ],
          "cluster_size": 3,
          "created": "2026-10-05T13:10:20",
          "encrypted": true,
          "engine": "valkey",
          "engine_config": {
            "backup_hour": 3,
            "backup_minute": 30,
            "frequent_snapshots": true,
            "valkey_persistence": "rdb"
          },
          "fork": {
            "restore_time": "2026-10-05T14:00:00",
            "source": 12344
          },
          "hosts": {
            "primary": "a225891-akamai-prod-1798333-default.g2a.akamaidb.net"
          },
          "id": 12345,
          "label": "my-db",
          "members": {
            "172.104.207.136": "primary"
          },
          "platform": "rdbms-default",
          "port": 11876,
          "private_network": {
            "public_access": true,
            "subnet_id": 456,
            "vpc_id": 123
          },
          "region": "us-mia",
          "ssl_connection": true,
          "status": "active",
          "total_disk_size_gb": 30,
          "type": "g6-dedicated-2",
          "updated": "2026-10-05T14:25:55",
          "updates": {
            "day_of_week": 4,
            "duration": 4,
            "frequency": "weekly",
            "hour_of_day": 16,
            "pending": []
          },
          "used_disk_size_gb": 0,
          "version": "8.1.0"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-valkey-instance) for a list of returned fields


- `ssl_cert` - The SSL CA certificate for an accessible Managed Valkey Database.

    - Sample Response:
        ```json
        {
          "ca_certificate": "LS0tLS1CRUdJ...=="
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-valkey-instance-ssl) for a list of returned fields


- `credentials` - The root username and password for an accessible Managed Valkey Database.

    - Sample Response:
        ```json
        {
          "password": "s3cur3P@ssw0rd",
          "username": "akmadmin"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-valkey-instance-credentials) for a list of returned fields


