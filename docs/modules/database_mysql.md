# database_mysql

Manage a Linode MySQL database.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a basic MySQL database
  linode.cloud.database_mysql:
    label: my-db
    region: us-east
    engine: mysql/8.0.26
    type: g6-standard-1
    allow_list:
      - 0.0.0.0/0
    state: present
```

```yaml
- name: Create a complex 3 node MySQL database
  linode.cloud.database_mysql:
    label: my-db
    region: us-east
    engine: mysql/8.0.26
    type: g6-standard-1
    allow_list:
      - 0.0.0.0/0
    encrypted: true
    cluster_size: 3
    replication_type: semi_synch
    ssl_connection: true
    state: present
```

```yaml
- name: Delete a MySQL database
  linode.cloud.database_mysql:
    label: my-db
    state: absent
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | `str` | **Required** | This database's unique label.   |
| `state` | `str` | **Required** | The state of this database.  (Choices:  `present`  `absent` ) |
| `allow_list` | `list` | Optional | A list of IP addresses that can access the Managed Database. Each item must be a range in CIDR format.   |
| `cluster_size` | `int` | Optional | The number of Linode Instance nodes deployed to the Managed Database.  (Choices:  `1`  `3` Default: `1`) |
| `encrypted` | `bool` | Optional | Whether the Managed Databases is encrypted.   |
| `engine` | `str` | Optional | The Managed Database engine in engine/version format.   |
| `region` | `str` | Optional | The Region ID for the Managed Database.   |
| `replication_type` | `str` | Optional | The replication method used for the Managed Database. Defaults to none for a single cluster and semi_synch for a high availability cluster. Must be none for a single node cluster. Must be asynch or semi_synch for a high availability cluster.  (Choices:  `none`  `asynch`  `semi_synch` Default: `none`) |
| `ssl_connection` | `bool` | Optional | Whether to require SSL credentials to establish a connection to the Managed Database.  (Default: `True`) |
| `type` | `str` | Optional | The Linode Instance type used by the Managed Database for its nodes.   |
| `wait` | `bool` | Optional | Wait for the database to have status `available` before returning.  (Default: `True`) |
| `wait_timeout` | `int` | Optional | The amount of time, in seconds, to wait for an image to have status `available`.  (Default: `3600`) |






## Return Values

- `database` - The database in JSON serialized form.

    - Sample Response:
        ```json
        {
          "allow_list": [
            "203.0.113.1/32",
            "192.0.1.0/24"
          ],
          "cluster_size": 3,
          "created": "2022-01-01T00:01:01",
          "encrypted": false,
          "engine": "mysql",
          "hosts": {
            "primary": "lin-123-456-mysql-mysql-primary.servers.linodedb.net",
            "secondary": "lin-123-456-mysql-primary-private.servers.linodedb.net"
          },
          "id": 123,
          "label": "example-db",
          "port": 3306,
          "region": "us-east",
          "replication_type": "semi_synch",
          "ssl_connection": true,
          "status": "active",
          "type": "g6-dedicated-2",
          "updated": "2022-01-01T00:01:01",
          "updates": {
            "day_of_week": 1,
            "duration": 3,
            "frequency": "weekly",
            "hour_of_day": 0,
            "week_of_month": null
          },
          "version": "8.0.26"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-mysql-database-view__response-samples) for a list of returned fields


- `backups` - The database backups in JSON serialized form.

    - Sample Response:
        ```json
        [
           {
              "created":"2022-01-01T00:01:01",
              "id":123,
              "label":"Scheduled - 02/04/22 11:11 UTC-XcCRmI",
              "type":"auto"
           }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-mysql-database-backup-view__responses) for a list of returned fields


- `ssl_cert` - The SSL CA certificate for an accessible Managed MySQL Database.

    - Sample Response:
        ```json
        {
          "ca_certificate": "LS0tLS1CRUdJ...=="
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-mysql-database-ssl-certificate-view__responses) for a list of returned fields


- `credentials` - The root username and password for an accessible Managed MySQL Database.

    - Sample Response:
        ```json
        {
          "password": "s3cur3P@ssw0rd",
          "username": "linroot"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-mysql-database-credentials-view__responses) for a list of returned fields


