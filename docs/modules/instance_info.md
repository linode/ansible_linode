# instance_info

Get info about a Linode Instance.

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
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Instance to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Instance to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `instance` - The returned Instance.

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
          "has_user_data": true,
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
          "maintenance_policy": "linode/migrate",
          "placement_group": {
            "id": 123,
            "label": "test",
            "placement_group_type": "anti_affinity:local",
            "placement_group_policy": "strict"
          }
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-instance) for a list of returned fields


- `configs` - The returned Configs.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-config) for a list of returned fields


- `disks` - The returned Disks.

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
            "updated": "2018-01-01T00:01:01",
            "disk_encryption": "enabled"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-disk) for a list of returned fields


- `networking` - The returned Networking Configuration.

    - Sample Response:
        ```json
        
        {
          "ipv4": {
            "private": [
              {
                "address": "192.168.133.234",
                "gateway": null,
                "linode_id": 123,
                "prefix": 17,
                "public": false,
                "rdns": null,
                "region": "us-east",
                "subnet_mask": "255.255.128.0",
                "type": "ipv4"
              }
            ],
            "public": [
              {
                "address": "97.107.143.141",
                "gateway": "97.107.143.1",
                "linode_id": 123,
                "prefix": 24,
                "public": true,
                "rdns": "test.example.org",
                "region": "us-east",
                "subnet_mask": "255.255.255.0",
                "type": "ipv4"
              }
            ],
            "reserved": [
              {
                "address": "97.107.143.141",
                "gateway": "97.107.143.1",
                "linode_id": 123,
                "prefix": 24,
                "public": true,
                "rdns": "test.example.org",
                "region": "us-east",
                "subnet_mask": "255.255.255.0",
                "type": "ipv4"
              }
            ],
            "shared": [
              {
                "address": "97.107.143.141",
                "gateway": "97.107.143.1",
                "linode_id": 123,
                "prefix": 24,
                "public": true,
                "rdns": "test.example.org",
                "region": "us-east",
                "subnet_mask": "255.255.255.0",
                "type": "ipv4"
              }
            ]
          },
          "ipv6": {
            "global": {
              "prefix": 124,
              "range": "2600:3c01::2:5000:0",
              "region": "us-east",
              "route_target": "2600:3c01::2:5000:f"
            },
            "link_local": {
              "address": "fe80::f03c:91ff:fe24:3a2f",
              "gateway": "fe80::1",
              "linode_id": 123,
              "prefix": 64,
              "public": false,
              "rdns": null,
              "region": "us-east",
              "subnet_mask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
              "type": "ipv6"
            },
            "slaac": {
              "address": "2600:3c03::f03c:91ff:fe24:3a2f",
              "gateway": "fe80::1",
              "linode_id": 123,
              "prefix": 64,
              "public": true,
              "rdns": null,
              "region": "us-east",
              "subnet_mask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
              "type": "ipv6"
            }
          }
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-ips) for a list of returned fields


