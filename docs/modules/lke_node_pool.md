# lke_node_pool

Manage Linode LKE cluster node pools.

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
| `cluster_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the LKE cluster that contains this node pool.   |
| `tags` | <center>`list`</center> | <center>**Required**</center> | An array of tags applied to this object. Tags must be unique as they are used by the `lke_node_pool` module to uniquely identify node pools.  **(Updatable)** |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| [`autoscaler` (sub-options)](#autoscaler) | <center>`dict`</center> | <center>Optional</center> | When enabled, the number of nodes autoscales within the defined minimum and maximum values.  **(Updatable)** |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of nodes in the Node Pool.  **(Updatable)** |
| [`disks` (sub-options)](#disks) | <center>`list`</center> | <center>Optional</center> | This Node Pool’s custom disk layout. Each item in this array will create a new disk partition for each node in this Node Pool.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The Linode Type for all of the nodes in the Node Pool. Required if `state` == `present`.   |
| `skip_polling` | <center>`bool`</center> | <center>Optional</center> | If true, the module will not wait for all nodes in the node pool to be ready.  **(Default: `False`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The period to wait for the node pool to be ready in seconds.  **(Default: `600`)** |
| `labels` | <center>`dict`</center> | <center>Optional</center> | Key-value pairs added as labels to nodes in the node pool. Labels help classify your nodes and to easily select subsets of objects.  **(Updatable)** |
| [`taints` (sub-options)](#taints) | <center>`list`</center> | <center>Optional</center> | Kubernetes taints to add to node pool nodes. Taints help control how pods are scheduled onto nodes, specifically allowing them to repel certain pods.  **(Updatable)** |
| `k8s_version` | <center>`str`</center> | <center>Optional</center> | The desired Kubernetes version for this Kubernetes  Node Pool in the format of <major>.<minor>, and the  latest supported patch version. NOTE: Only available for LKE Enterprise to support node pool upgrades.  This field may not currently be available to all users and is under v4beta.  **(Updatable)** |
| `update_strategy` | <center>`str`</center> | <center>Optional</center> | Upgrade strategy describes the available upgrade strategies. NOTE: Only available for LKE Enterprise to support node pool upgrades.  This field may not currently be available to all users and is under v4beta.  **(Choices: `rolling_update`, `on_recycle`; Updatable)** |

### autoscaler

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `enabled` | <center>`bool`</center> | <center>Optional</center> | Whether autoscaling is enabled for this Node Pool. NOTE: Subsequent playbook runs will override nodes created by the cluster autoscaler.  **(Updatable)** |
| `max` | <center>`int`</center> | <center>Optional</center> | The maximum number of nodes to autoscale to. Defaults to the value provided by the count field.  **(Updatable)** |
| `min` | <center>`int`</center> | <center>Optional</center> | The minimum number of nodes to autoscale to. Defaults to the Node Pool’s count.  **(Updatable)** |

### disks

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `type` | <center>`str`</center> | <center>**Required**</center> | This custom disk partition’s filesystem type.  **(Choices: `raw`, `ext4`)** |
| `size` | <center>`int`</center> | <center>**Required**</center> | The size of this custom disk partition in MB.   |

### taints

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `key` | <center>`str`</center> | <center>**Required**</center> | The Kubernetes taint key.  **(Updatable)** |
| `value` | <center>`str`</center> | <center>**Required**</center> | The Kubernetes taint value.  **(Updatable)** |
| `effect` | <center>`str`</center> | <center>**Required**</center> | The Kubernetes taint effect.  **(Choices: `NoSchedule`, `PreferNoSchedule`, `NoExecute`; Updatable)** |

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
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-node-pool) for a list of returned fields


