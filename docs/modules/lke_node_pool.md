# lke_node_pool

Manage Linode LKE cluster node pools.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a Linode LKE node pool
  linode.cloud.lke_node_pool:
    cluster_id: 12345
  
    tags: ['my-pool']
    count: 3
    type: g6-standard-2
    state: present
```

```yaml
- name: Create a Linode LKE node pool with autoscaler
  linode.cloud.lke_node_pool:
    cluster_id: 12345
  
    tags: ['my-pool']
    count: 3
    type: g6-standard-2
    
    autoscaler:
        enabled: true
        min: 1
        max: 3

    state: present
- name: Delete a Linode LKE node pool
  linode.cloud.lke_node_pool:
    cluster_id: 12345
    tags: ['my-pool']
    state: absent
```









## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `cluster_id` | `int` | **Required** | The ID of the LKE cluster that contains this node pool.   |
| `count` | `int` | **Required** | The number of nodes in the Node Pool.   |
| `tags` | `list` | **Required** | An array of tags applied to this object. Tags must be unique as they are used by the `lke_node_pool` module to uniquely identify node pools.   |
| `state` | `str` | **Required** | The desired state of the target.  (Choices:  `present` `absent`) |
| [`autoscaler` (sub-options)](#autoscaler) | `dict` | Optional | When enabled, the number of nodes autoscales within the defined minimum and maximum values.   |
| [`disks` (sub-options)](#disks) | `list` | Optional | This Node Pool’s custom disk layout. Each item in this array will create a new disk partition for each node in this Node Pool.   |
| `type` | `str` | Optional | The Linode Type for all of the nodes in the Node Pool. Required if `state` == `present`.   |
| `skip_polling` | `bool` | Optional | If true, the module will not wait for all nodes in the node pool to be ready.   |
| `wait_timeout` | `int` | Optional | The period to wait for the node pool to be ready in seconds.  ( Default: `600`) |





### autoscaler

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `enabled` | `bool` | Optional | Whether autoscaling is enabled for this Node Pool. NOTE: Subsequent playbook runs will override nodes created by the cluster autoscaler.   |
| `max` | `int` | Optional | The maximum number of nodes to autoscale to. Defaults to the value provided by the count field.   |
| `min` | `int` | Optional | The minimum number of nodes to autoscale to. Defaults to the Node Pool’s count.   |





### disks

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `type` | `str` | **Required** | This custom disk partition’s filesystem type.  (Choices:  `raw` `ext4`) |
| `size` | `int` | **Required** | The size of this custom disk partition in MB.   |





## Return Values

- `node_pool` - The Node Pool in JSON serialized form.

    - Sample Response:
        ```json
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
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#node-pool-view__response-samples) for a list of returned fields


