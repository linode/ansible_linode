"""Documentation fragments for the instance_list module"""

specdoc_examples = ['''
- name: List all of the instances for the current Linode Account
  linode.cloud.instance_list: {}''', '''
- name: Resolve all instances for the current Linode Account
  linode.cloud.instance_list:
    filters:
      - name: label
        values: myInstanceLabel''']

result_instances_samples = ['''[
   {
      "alerts": {
        "cpu": 180,
        "io": 10000,
        "network_in": 10,
        "network_out": 10,
        "transfer_quota": 80
      },
      "backups": {
        "available": true,
        "enabled": true,
        "last_successful": "2018-01-01T00:01:01",
        "schedule": {
          "day": "Saturday",
          "window": "W22"
        }
      },
      "created": "2018-01-01T00:01:01",
      "group": "Linode-Group",
      "host_uuid": "example-uuid",
      "hypervisor": "kvm",
      "id": 123,
      "image": "linode/debian11",
      "ipv4": [
        "203.0.113.1",
        "192.0.2.1"
      ],
      "ipv6": "c001:d00d::1337/128",
      "label": "linode123",
      "region": "us-east",
      "specs": {
        "disk": 81920,
        "memory": 4096,
        "transfer": 4000,
        "vcpus": 2
      },
      "status": "running",
      "tags": [
        "example tag",
        "another example"
      ],
      "type": "g6-standard-1",
      "updated": "2018-01-01T00:01:01",
      "watchdog_enabled": true,
      "disk_encryption": "enabled",
      "lke_cluster_id": null,
      "maintenance_policy": "linode/migrate"
    }
]''']
