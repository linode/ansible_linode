"""Documentation fragments for the lke_cluster module"""

examples = ['''
- name: Create a Linode LKE node pool
  linode.cloud.lke_node_pool:
    cluster_id: 12345
  
    tags: ['my-pool']
    count: 3
    type: g6-standard-2
    state: present''', '''
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

    state: present''' '''
- name: Delete a Linode LKE node pool
  linode.cloud.lke_node_pool:
    cluster_id: 12345
    tags: ['my-pool']
    state: absent''']

result_node_pool = ['''{
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
}''']
