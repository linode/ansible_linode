"""Documentation fragments for the instance module"""

specdoc_examples = ['''
- name: Create a new Linode instance.
  linode.cloud.instance:
    label: my-linode
    type: g6-nanode-1
    region: us-east
    image: linode/ubuntu20.04
    root_pass: verysecurepassword!!!
    private_ip: false
    authorized_keys:
      - "ssh-rsa ..."
    stackscript_id: 1337
    stackscript_data:
      variable: value
    group: app
    tags:
      - env=prod
    state: present''', '''
- name: Delete a Linode instance.
  linode.cloud.instance:
    label: my-linode
    state: absent''']

result_instance_samples = ['''{
  "alerts": {
    "cpu": 180,
    "io": 10000,
    "network_in": 10,
    "network_out": 10,
    "transfer_quota": 80
  },
  "backups": {
    "enabled": true,
    "last_successful": "2018-01-01T00:01:01",
    "schedule": {
      "day": "Saturday",
      "window": "W22"
    }
  },
  "created": "2018-01-01T00:01:01",
  "group": "Linode-Group",
  "hypervisor": "kvm",
  "id": 123,
  "image": "linode/debian10",
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
  "watchdog_enabled": true
}''']

result_configs_samples = ['''[
  {
    "comments": "This is my main Config",
    "devices": {
      "sda": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdb": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdc": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdd": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sde": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdf": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdg": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdh": {
        "disk_id": 124458,
        "volume_id": null
      }
    },
    "helpers": {
      "devtmpfs_automount": false,
      "distro": true,
      "modules_dep": true,
      "network": true,
      "updatedb_disabled": true
    },
    "id": 23456,
    "interfaces": [
      {
        "ipam_address": "10.0.0.1/24",
        "label": "example-interface",
        "purpose": "vlan"
      }
    ],
    "kernel": "linode/latest-64bit",
    "label": "My Config",
    "memory_limit": 2048,
    "root_device": "/dev/sda",
    "run_level": "default",
    "virt_mode": "paravirt"
  }
]''']

result_disks_samples = ['''[
  {
    "created": "2018-01-01T00:01:01",
    "filesystem": "ext4",
    "id": 25674,
    "label": "Debian 9 Disk",
    "size": 48640,
    "status": "ready",
    "updated": "2018-01-01T00:01:01"
  }
]''']
