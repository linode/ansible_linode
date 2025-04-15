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
- name: Create a PostgreSQL database with an explicit maintenance schedule
  linode.cloud.database_postgresql_v2:
    label: my-db
    region: us-mia
    engine: postgresql/16
    type: g6-nanode-1
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
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the Managed Database.  **(Choices: `present`, `absent`)** |
| `allow_list` | <center>`list`</center> | <center>Optional</center> | A list of IP addresses and CIDR ranges that can access the Managed Database.  **(Updatable)** |
| `cluster_size` | <center>`int`</center> | <center>Optional</center> | The number of Linode instance nodes deployed to the Managed Database.  **(Updatable)** |
| `engine` | <center>`str`</center> | <center>Optional</center> | The Managed Database engine in engine/version format.  **(Updatable)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Managed Database.   |
| `region` | <center>`str`</center> | <center>Optional</center> | The region of the Managed Database.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The Linode Instance type used by the Managed Database for its nodes.  **(Updatable)** |
| [`fork` (sub-options)](#fork) | <center>`dict`</center> | <center>Optional</center> | Information about a database to fork from.   |
| [`updates` (sub-options)](#updates) | <center>`dict`</center> | <center>Optional</center> | Configuration settings for automated patch update maintenance for the Managed Database.  **(Updatable)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The maximum number of seconds a poll operation can take before raising an error.  **(Default: `2700`)** |

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


