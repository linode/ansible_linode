# lke_cluster_info

Get info about a Linode LKE cluster.

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
- name: Get info about an LKE cluster by label
  linode.cloud.lke_cluster_info:
    label: 'my-cluster' 
```

```yaml
- name: Get info about an LKE cluster by ID
  linode.cloud.lke_cluster_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the LKE cluster. Optional if `label` is defined.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the LKE cluster. Optional if `id` is defined.  **(Conflicts With: `id`)** |

## Return Values

- `cluster` - The LKE cluster in JSON serialized form.

    - Sample Response:
        ```json
        {
          "control_plane": {
            "acl": {
                "addresses": {
                    "ipv4": ["0.0.0.0/0"], 
                    "ipv6": ["2001:db8:1234:abcd::/64"]
                }, 
                "enabled": true
            },
            "high_availability": true
          },
          "created": "2019-09-12T21:25:30Z",
          "id": 1234,
          "k8s_version": "1.28",
          "label": "lkecluster12345",
          "region": "us-central",
          "tags": [
            "ecomm",
            "blogs"
          ],
          "updated": "2019-09-13T21:24:16Z"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-cluster) for a list of returned fields


- `node_pools` - A list of node pools in JSON serialized form.

    - Sample Response:
        ```json
        [
          {
            "autoscaler": {
              "enabled": true,
              "max": 12,
              "min": 3
            },
            "disk_encryption": "enabled",
            "count": 6,
            "disks": [
              {
                "size": 1024,
                "type": "ext-4"
              }
            ],
            "id": 456,
            "nodes": [
              {
                "id": "123456",
                "instance_id": 123458,
                "status": "ready"
              }
            ],
            "tags": [
              "example tag",
              "another example"
            ],
            "type": "g6-standard-4"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-cluster-pools) for a list of returned fields


- `kubeconfig` - The Base64-encoded kubeconfig used to access this cluster. 
NOTE: This value may be unavailable if the cluster is not fully provisioned.

    - Sample Response:
        ```json
        "a3ViZWNvbmZpZyBjb250ZW50Cg=="
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-cluster-kubeconfig) for a list of returned fields


- `dashboard_url` - The Cluster Dashboard access URL.

    - Sample Response:
        ```json
        "https://example.dashboard.linodelke.net"
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-cluster-dashboard) for a list of returned fields


