# instance_info

Get info about a Linode Instance.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about an instance by label
  linode.cloud.instance_info:
    label: 'my-instance' 
```

```yaml
- name: Get info about an instance by id
  linode.cloud.instance_info:
    id: 12345
```









## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | `int` | Optional | The instance’s label. Optional if `label` is defined.   |
| `label` | `str` | Optional | The unique ID of the Instance. Optional if `id` is defined.   |





## Return Values

- `instance` - The instance description in JSON serialized form.

    - Sample Response:
        ```json
        {
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
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-instances/#linode-view__responses) for a list of returned fields


- `configs` - A list of configs tied to this Linode Instance.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-instances/#configuration-profile-view__responses) for a list of returned fields


- `disks` - A list of disks tied to this Linode Instance.

    - Sample Response:
        ```json
        [
          {
            "created": "2018-01-01T00:01:01",
            "filesystem": "ext4",
            "id": 25674,
            "label": "Debian 9 Disk",
            "size": 48640,
            "status": "ready",
            "updated": "2018-01-01T00:01:01"
          }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-instances/#disk-view__responses) for a list of returned fields


