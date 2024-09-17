# object_cluster_list

**NOTE: This module has been deprecated because it relies on deprecated API endpoints. Going forward, `region` will be the preferred way to designate where Object Storage resources should be created.**

List and filter on Object Storage Clusters.

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
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Object Storage Clusters in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Object Storage Clusters by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Object Storage Clusters.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Object Storage Clusters to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-object-storage-clusters).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `clusters` - The returned Object Storage Clusters.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-clusters) for a list of returned fields


