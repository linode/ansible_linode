# database_postgresql_info

Get info about a Linode PostgreSQL Managed Database.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about a Managed PostgreSQL Database by label
  linode.cloud.database_postgresql_info:
    label: my-db
```

```yaml
- name: Get info about a Managed PostgreSQL Database by ID
  linode.cloud.database_postgresql_info:
    id: 12345
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | The ID of the PostgreSQL Database.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the PostgreSQL Database.  **(Conflicts With: `id`)** |






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
          "engine": "postgresql",
          "hosts": {
            "primary": "lin-0000-000-pgsql-primary.servers.linodedb.net",
            "secondary": "lin-0000-000-pgsql-primary-private.servers.linodedb.net"
          },
          "id": 123,
          "label": "example-db",
          "port": 3306,
          "region": "us-east",
          "replication_commit_type": "local",
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
          "version": "13.2"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-postgresql-database-view__response-samples) for a list of returned fields


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-postgresql-database-backups-list__response-samples) for a list of returned fields


- `ssl_cert` - The SSL CA certificate for an accessible Managed PostgreSQL Database.

    - Sample Response:
        ```json
        {
          "ca_certificate": "LS0tLS1CRUdJ...=="
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-postgresql-database-ssl-certificate-view) for a list of returned fields


- `credentials` - The root username and password for an accessible Managed PostgreSQL Database.

    - Sample Response:
        ```json
        {
          "password": "s3cur3P@ssw0rd",
          "username": "linroot"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-postgresql-database-credentials-view__request-samples) for a list of returned fields


