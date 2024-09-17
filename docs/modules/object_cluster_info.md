# object_cluster_info

**NOTE: This module has been deprecated because it relies on deprecated API endpoints. Going forward, `region` will be the preferred way to designate where Object Storage resources should be created.**

Get info about a Linode Object Storage Cluster.

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
- name: Get info about clusters in us-east
  linode.cloud.object_cluster_info:
    region: us-east
```

```yaml
- name: Get info about the cluster with id us-east-1
  linode.cloud.object_cluster_info:
    id: us-east-1
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | The unique id given to the clusters.   |
| `region` | <center>`str`</center> | <center>Optional</center> | The region the clusters are in.   |
| `domain` | <center>`str`</center> | <center>Optional</center> | The domain of the clusters.   |
| `static_site_domain` | <center>`str`</center> | <center>Optional</center> | The static-site domain of the clusters.   |

## Return Values

- `clusters` - The Object Storage clusters in JSON serialized form.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-cluster) for a list of returned fields


