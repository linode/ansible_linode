# lke_cluster

Manage Linode LKE clusters.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a Linode LKE cluster
  linode.cloud.lke_cluster:
    label: 'my-cluster'
    region: us-southeast
    k8s_version: 1.28
    node_pools:
      - type: g6-standard-1
        count: 3
      - type: g6-standard-2
        count: 2
    state: present
```

```yaml
- name: Create a Linode LKE cluster with autoscaler
  linode.cloud.lke_cluster:
    label: 'my-cluster'
    region: us-southeast
    k8s_version: 1.28
    node_pools:
      - type: g6-standard-1
        count: 2
        autoscaler:
          enable: true
          min: 2
          max: 5
    state: present
```

```yaml
- name: Delete a Linode LKE cluster
  linode.cloud.lke_cluster:
    label: 'my-cluster'
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This Kubernetes cluster’s unique label.   |
| `k8s_version` | <center>`str`</center> | <center>Optional</center> | The desired Kubernetes version for this Kubernetes cluster in the format of <major>.<minor>, and the latest supported patch version will be deployed. A version upgrade requires that you manually recycle the nodes in your cluster.  **(Updatable)** |
| `region` | <center>`str`</center> | <center>Optional</center> | This Kubernetes cluster’s location.   |
| `tags` | <center>`list`</center> | <center>Optional</center> | An array of tags applied to the Kubernetes cluster.   |
| `high_availability` | <center>`bool`</center> | <center>Optional</center> | Defines whether High Availability is enabled for the Control Plane Components of the cluster.   **(Default: `False`; Updatable)** |
| [`node_pools` (sub-options)](#node_pools) | <center>`list`</center> | <center>Optional</center> | A list of node pools to configure the cluster with  **(Updatable)** |
| `skip_polling` | <center>`bool`</center> | <center>Optional</center> | If true, the module will not wait for all nodes in the cluster to be ready.  **(Default: `False`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The period to wait for the cluster to be ready in seconds.  **(Default: `600`)** |

### node_pools

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `count` | <center>`int`</center> | <center>**Required**</center> | The number of nodes in the Node Pool.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>**Required**</center> | The Linode Type for all of the nodes in the Node Pool.   |
| [`autoscaler` (sub-options)](#autoscaler) | <center>`dict`</center> | <center>Optional</center> | When enabled, the number of nodes autoscales within the defined minimum and maximum values.  **(Updatable)** |

### autoscaler

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `enabled` | <center>`bool`</center> | <center>Optional</center> | Whether autoscaling is enabled for this Node Pool. NOTE: Subsequent playbook runs will override nodes created by the cluster autoscaler.  **(Updatable)** |
| `max` | <center>`int`</center> | <center>Optional</center> | The maximum number of nodes to autoscale to. Defaults to the value provided by the count field.  **(Updatable)** |
| `min` | <center>`int`</center> | <center>Optional</center> | The minimum number of nodes to autoscale to. Defaults to the Node Pool’s count.  **(Updatable)** |

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


- `kubeconfig` - The Base64-encoded kubeconfig used to access this cluster. 
NOTE: This value may be unavailable if `skip_polling` is true.
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#kubeconfig-view__responses) for a list of returned fields


- `dashboard_url` - The Cluster Dashboard access URL.
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#kubernetes-cluster-dashboard-url-view__responses) for a list of returned fields


