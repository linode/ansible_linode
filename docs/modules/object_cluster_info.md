# object_cluster_info

Get info about a Linode Object Storage Cluster.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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



- `id` (`str`) -  The unique id given to the clusters.  
- `region` (`str`) -  The region the clusters are in.  
- `domain` (`str`) -  The domain of the clusters.  
- `static_site_domain` (`str`) -  The static-site domain of the clusters.  


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/object-storage/#cluster-view__responses) for a list of returned fields


