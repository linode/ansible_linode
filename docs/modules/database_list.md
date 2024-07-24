# database_list

List and filter on Linode Managed Databases.

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
- name: List all of the databases for the current Linode Account
  linode.cloud.database_list: {}
```

```yaml
- name: Resolve all MySQL databases for the current Linode Account
  linode.cloud.database_list:
    filters:
      - name: engine
        values: mysql
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list databases in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order databases by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting databases.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://techdocs.akamai.com/linode-api/reference/get-databases-engines   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `databases` - The returned database.

    - Sample Response:
        ```json
        [
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
              "instance_uri": "/v4/databases/mysql/instances/123",
              "label": "example-db",
              "region": "us-east",
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
              "version": "8.0.30"
           }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-databases-instances) for a list of returned fields


