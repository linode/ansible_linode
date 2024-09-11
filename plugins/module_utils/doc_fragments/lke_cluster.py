"""Documentation fragments for the lke_cluster module"""

examples = ['''
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
    state: present''', '''
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
    state: present''', '''
- name: Delete a Linode LKE cluster
  linode.cloud.lke_cluster:
    label: 'my-cluster'
    state: absent''']

result_cluster = ['''{
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
}''']

result_node_pools = ['''[
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
]''']
