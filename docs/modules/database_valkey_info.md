# database_valkey_info

Get info about a Linode Valkey Managed Database.

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
- name: Get info about a Managed Valkey Database by label
  linode.cloud.database_valkey_info:
    label: my-db
```

```yaml
- name: Get info about a Managed Valkey Database by ID
  linode.cloud.database_valkey_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | The ID of the Valkey Database.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Valkey Database.  **(Conflicts With: `id`)** |

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


