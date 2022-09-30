# lke_cluster_info

Get info about a Linode LKE cluster.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `id` | `int` | Optional | The ID of the LKE cluster. Optional if `label` is defined.   |
| `label` | `str` | Optional | The label of the LKE cluster. Optional if `id` is defined.   |






## Return Values

- `cluster` - The LKE cluster in JSON serialized form.

    - Sample Response:
        ```json
        {
          "control_plane": {
            "high_availability": true
          },
          "created": "2019-09-12T21:25:30Z",
          "id": 1234,
          "k8s_version": "1.23",
          "label": "lkecluster12345",
          "region": "us-central",
          "tags": [
            "ecomm",
            "blogs"
          ],
          "updated": "2019-09-13T21:24:16Z"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#kubernetes-cluster-view__response-samples) for a list of returned fields


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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#node-pools-list__response-samples) for a list of returned fields


- `kubeconfig` - The Base64-encoded kubeconfig used to access this cluster.NOTE: This value may be unavailable if the cluster is not fully provisioned.
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#kubeconfig-view__responses) for a list of returned fields


- `dashboard_url` - The Cluster Dashboard access URL.
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#kubernetes-cluster-dashboard-url-view__responses) for a list of returned fields


