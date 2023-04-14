# database_engine_list

List and filter on Managed Database engine types.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the available Managed Database engine types
  linode.cloud.database_engine_list: {}
```

```yaml
- name: Resolve all Database engine types
  linode.cloud.database_engine_list:
    filters:
      - name: engine
        values: mysql
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list database engine types in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order database engine types by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting database engine types.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/databases/#managed-database-engines-list__responses   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `engines` - The returned database engine types.

    - Sample Response:
        ```json
        [
           {
              "engine": "mysql",
              "id": "mysql/8.0.30",
              "version": "8.0.30"
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/databases/#managed-database-engines-list__response-samples) for a list of returned fields


