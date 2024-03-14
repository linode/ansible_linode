# object_cluster_list

List and filter on Object Storage Clusters.

LINODE_API_TOKEN environment variable is required.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the object storage clusters for the current Linode Account
  linode.cloud.object_cluster_list: {}
```

```yaml
- name: Resolve all object storage clusters for the current Linode Account
  linode.cloud.object_cluster_list:
    filters:
      - name: region
        values: us-east
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list object storage clusters in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order object storage clusters by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting object storage clusters.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/object-storage/#clusters-list__responses   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `clusters` - The returned object storage clusters.

    - Sample Response:
        ```json
        [
          {
            "domain": "us-east-1.linodeobjects.com",
            "id": "us-east-1",
            "region": "us-east",
            "static_site_domain": "website-us-east-1.linodeobjects.com",
            "status": "available"
          }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/object-storage/#clusters-list__response-samples) for a list of returned fields


