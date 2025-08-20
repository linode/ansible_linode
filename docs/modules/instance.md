# instance

Manage Linode Instances, Configs, and Disks.

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
- name: Create a new Linode instance.
  linode.cloud.instance:
    label: my-linode
    type: g6-nanode-1
    region: us-east
    image: linode/ubuntu22.04
    root_pass: verysecurepassword!!!
    private_ip: false
    authorized_keys:
      - "ssh-rsa ..."
    stackscript_id: 1337
    stackscript_data:
      variable: value
    tags:
      - env=prod
    state: present
```

```yaml
- name: Create a new Linode instance with an additional public IPv4 address.
  linode.cloud.instance:
    label: my-linode
    type: g6-nanode-1
    region: us-east
    image: linode/ubuntu22.04
    root_pass: verysecurepassword!!!
    private_ip: false
    authorized_keys:
      - "ssh-rsa ..."
    stackscript_id: 1337
    stackscript_data:
      variable: value
    tags:
      - env=prod
    state: present
    additional_ipv4:
      - public: true
```

```yaml
- name: Create a Linode Instance with explicit configs and disks.
  linode.cloud.instance:
    label: 'my-complex-instance'
    region: us-southeast
    type: g6-standard-1
    booted: true
    boot_config_label: boot-config
    state: present
    disks:
      - label: boot
        image: linode/ubuntu22.04
        size: 3000
        root_pass: ans1ble-test!
      - label: swap
        filesystem: swap
        size: 512
    configs:
      - label: boot-config
        root_device: /dev/sda
        devices:
          sda:
            disk_label: boot
          sdb:
            disk_label: swap
        state: present
```

```yaml
- name: Create a Linode Instance with custom user data.
  linode.cloud.instance:
    label: 'my-metadata-instance'
    region: us-southeast
    type: g6-standard-1
    image: linode/ubuntu22.04
    root_pass: verysecurepassword!!!
    metadata:
      user_data: myuserdata
    state: present
```

```yaml
- name: Create a new Linode instance under a placement group.
  linode.cloud.instance:
    label: my-linode
    type: g6-nanode-1
    region: us-east
    placement_group:
      id: 123
      compliant_only: false
    state: present
```

```yaml
- name: Delete a Linode instance.
  linode.cloud.instance:
    label: my-linode
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The unique label to give this instance.   |
| `type` | <center>`str`</center> | <center>Optional</center> | The Linode Type of the Linode you are creating.   |
| `region` | <center>`str`</center> | <center>Optional</center> | The location to deploy the instance in. See the [Linode API documentation](https://api.linode.com/v4/regions).   |
| `image` | <center>`str`</center> | <center>Optional</center> | The image ID to deploy the instance disk from.  **(Conflicts With: `disks`,`configs`)** |
| `authorized_keys` | <center>`list`</center> | <center>Optional</center> | A list of SSH public key parts to deploy for the root user.   |
| `authorized_users` | <center>`list`</center> | <center>Optional</center> | A list of usernames.   |
| `maintenance_policy` | <center>`str`</center> | <center>Optional</center> | The slug of the maintenance policy to apply during maintenance. NOTE: This field is under v4beta.  **(Choices: `linode/migrate`, `linode/power_off_on`)** |
| `root_pass` | <center>`str`</center> | <center>Optional</center> | The password for the root user. If not specified, one will be generated. This generated password will be available in the task success JSON.   |
| `stackscript_id` | <center>`int`</center> | <center>Optional</center> | The ID of the StackScript to use when creating the instance. See the [Linode API documentation](https://techdocs.akamai.com/linode-api/reference/get-stack-scripts).   |
| `stackscript_data` | <center>`dict`</center> | <center>Optional</center> | An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance. Only valid when a stackscript_id is provided. See the [Linode API documentation](https://techdocs.akamai.com/linode-api/reference/get-stack-scripts).   |
| `firewall_id` | <center>`int`</center> | <center>Optional</center> | The ID of a Firewall this Linode to assign this Linode to.   |
| `private_ip` | <center>`bool`</center> | <center>Optional</center> | If true, the created Linode will have private networking enabled.   |
| `group` | <center>`str`</center> | <center>Optional</center> | The group that the instance should be marked under. Please note, that group labelling is deprecated but still supported. The encouraged method for marking instances is to use tags.  **(Updatable)** |
| `boot_config_label` | <center>`str`</center> | <center>Optional</center> | The label of the config to boot from.   |
| [`configs` (sub-options)](#configs) | <center>`list`</center> | <center>Optional</center> | A list of Instance configs to apply to the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#configuration-profile-create).  **(Updatable; Conflicts With: `image`,`interfaces`)** |
| [`disks` (sub-options)](#disks) | <center>`list`</center> | <center>Optional</center> | A list of Disks to create on the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#disk-create).  **(Updatable; Conflicts With: `image`,`interfaces`)** |
| [`interfaces` (sub-options)](#interfaces) | <center>`list`</center> | <center>Optional</center> | A list of network interfaces to apply to the Linode. See the [Linode API documentation](https://techdocs.akamai.com/linode-api/reference/post-linode-instance).  **(Conflicts With: `disks`,`configs`)** |
| `booted` | <center>`bool`</center> | <center>Optional</center> | Whether the new Instance should be booted. This will default to True if the Instance is deployed from an Image or Backup.   |
| `backup_id` | <center>`int`</center> | <center>Optional</center> | The id of the Backup to restore to the new Instance. May not be provided if "image" is given.   |
| [`metadata` (sub-options)](#metadata) | <center>`dict`</center> | <center>Optional</center> | Fields relating to the Linode Metadata service.   |
| `backups_enabled` | <center>`bool`</center> | <center>Optional</center> | Enroll Instance in Linode Backup service.   |
| `wait` | <center>`bool`</center> | <center>Optional</center> | Wait for the instance to have status "running" before returning.  **(Default: `True`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The amount of time, in seconds, to wait for an instance to have status "running".  **(Default: `1500`)** |
| [`additional_ipv4` (sub-options)](#additional_ipv4) | <center>`list`</center> | <center>Optional</center> | Additional ipv4 addresses to allocate.   |
| `rebooted` | <center>`bool`</center> | <center>Optional</center> | If true, the Linode Instance will be rebooted. NOTE: The instance will only be rebooted if it was previously in a running state. To ensure your Linode will always be rebooted, consider also setting the `booted` field.  **(Default: `False`)** |
| `migration_type` | <center>`str`</center> | <center>Optional</center> | The type of migration to use for Region and Type migrations.  **(Choices: `cold`, `warm`; Default: `cold`)** |
| `auto_disk_resize` | <center>`bool`</center> | <center>Optional</center> | Whether implicitly created disks should be resized during a type change operation.  **(Default: `False`)** |
| `tags` | <center>`list`</center> | <center>Optional</center> | An array of tags applied to this object. Tags are for organizational purposes only.  **(Updatable)** |
| `capabilities` | <center>`list`</center> | <center>Optional</center> | Read-only. A list of capabilities this compute instance supports.   |
| [`placement_group` (sub-options)](#placement_group) | <center>`dict`</center> | <center>Optional</center> | A Placement Group to create this Linode under.   |
| `disk_encryption` | <center>`str`</center> | <center>Optional</center> | The disk encryption status of this Linode. NOTE: Disk encryption may not currently be available to all users.  **(Choices: `enabled`, `disabled`)** |
| `swap_size` | <center>`int`</center> | <center>Optional</center> | When deploying from an Image, this field is optional, otherwise it is ignored. This is used to set the swap disk size for the newly-created Linode.   |

### configs

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`devices` (sub-options)](#devices) | <center>`dict`</center> | <center>**Required**</center> | The devices to map to this configuration.   |
| `label` | <center>`str`</center> | <center>**Required**</center> | The label to assign to this config.   |
| `comments` | <center>`str`</center> | <center>Optional</center> | Arbitrary User comments on this Config.  **(Updatable)** |
| [`helpers` (sub-options)](#helpers) | <center>`dict`</center> | <center>Optional</center> | Helpers enabled when booting to this Linode Config.   |
| `kernel` | <center>`str`</center> | <center>Optional</center> | A Kernel ID to boot a Linode with. Defaults to "linode/latest-64bit".  **(Updatable)** |
| `memory_limit` | <center>`int`</center> | <center>Optional</center> | Defaults to the total RAM of the Linode.  **(Updatable)** |
| `root_device` | <center>`str`</center> | <center>Optional</center> | The root device to boot.  **(Updatable)** |
| `run_level` | <center>`str`</center> | <center>Optional</center> | Defines the state of your Linode after booting.  **(Updatable)** |
| `virt_mode` | <center>`str`</center> | <center>Optional</center> | Controls the virtualization mode.  **(Choices: `paravirt`, `fullvirt`; Updatable)** |
| [`interfaces` (sub-options)](#interfaces) | <center>`list`</center> | <center>Optional</center> | A list of network interfaces to apply to the Linode. See the [Linode API documentation](https://techdocs.akamai.com/linode-api/reference/post-add-linode-config).  **(Updatable)** |

### devices

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`sda` (sub-options)](#sda) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sda   |
| [`sdb` (sub-options)](#sdb) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sdb   |
| [`sdc` (sub-options)](#sdc) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sdc   |
| [`sdd` (sub-options)](#sdd) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sdd   |
| [`sde` (sub-options)](#sde) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sde   |
| [`sdf` (sub-options)](#sdf) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sdf   |
| [`sdg` (sub-options)](#sdg) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sdg   |
| [`sdh` (sub-options)](#sdh) | <center>`dict`</center> | <center>Optional</center> | The device to be mapped to /dev/sdh   |

### sda

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### sdb

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### sdc

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### sdd

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### sde

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### sdf

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### sdg

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### sdh

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `disk_label` | <center>`str`</center> | <center>Optional</center> | The label of the disk to attach to this Linode.   |
| `disk_id` | <center>`int`</center> | <center>Optional</center> | The ID of the disk to attach to this Linode.   |
| `volume_id` | <center>`int`</center> | <center>Optional</center> | The ID of the volume to attach to this Linode.   |

### helpers

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `devtmpfs_automount` | <center>`bool`</center> | <center>Optional</center> | Populates the /dev directory early during boot without udev.   |
| `distro` | <center>`bool`</center> | <center>Optional</center> | Helps maintain correct inittab/upstart console device.   |
| `modules_dep` | <center>`bool`</center> | <center>Optional</center> | Creates a modules dependency file for the Kernel you run.   |
| `network` | <center>`bool`</center> | <center>Optional</center> | Automatically configures static networking.   |
| `updatedb_disabled` | <center>`bool`</center> | <center>Optional</center> | Disables updatedb cron job to avoid disk thrashing.   |

### interfaces

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `purpose` | <center>`str`</center> | <center>**Required**</center> | The type of interface.  **(Choices: `public`, `vlan`, `vpc`)** |
| `primary` | <center>`bool`</center> | <center>Optional</center> | Whether this is a primary interface  **(Default: `False`)** |
| `subnet_id` | <center>`int`</center> | <center>Optional</center> | The ID of the VPC subnet to assign this interface to.   |
| `ipv4` | <center>`dict`</center> | <center>Optional</center> | The IPv4 configuration for this interface. (VPC only)   |
| `label` | <center>`str`</center> | <center>Optional</center> | The name of this interface. Required for vlan purpose interfaces. Must be an empty string or null for public purpose interfaces.   |
| `ipam_address` | <center>`str`</center> | <center>Optional</center> | This Network Interface’s private IP address in Classless Inter-Domain Routing (CIDR) notation.   |
| `ip_ranges` | <center>`list`</center> | <center>Optional</center> | Packets to these CIDR ranges are routed to the VPC network interface. (VPC only)   |

### disks

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | The label to give this Disk.   |
| `size` | <center>`int`</center> | <center>**Required**</center> | The size of the Disk in MB.  **(Updatable)** |
| `authorized_keys` | <center>`list`</center> | <center>Optional</center> | A list of SSH public key parts to deploy for the root user.   |
| `authorized_users` | <center>`list`</center> | <center>Optional</center> | A list of usernames.   |
| `filesystem` | <center>`str`</center> | <center>Optional</center> | The filesystem to create this disk with.   |
| `disk_encryption` | <center>`str`</center> | <center>Optional</center> | **READ ONLY** The disk encryption status of this disk.NOTE: Disk encryption may not currently be available to all users and is set at the Linode Level.  **(Choices: `enabled`, `disabled`)** |
| `image` | <center>`str`</center> | <center>Optional</center> | An Image ID to deploy the Disk from.   |
| `root_pass` | <center>`str`</center> | <center>Optional</center> | The root user’s password on the newly-created Linode.   |
| `stackscript_id` | <center>`int`</center> | <center>Optional</center> | The ID of the StackScript to use when creating the instance. See the [Linode API documentation](https://techdocs.akamai.com/linode-api/reference/get-stack-scripts).   |
| `stackscript_data` | <center>`dict`</center> | <center>Optional</center> | An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance. Only valid when a stackscript_id is provided. See the [Linode API documentation](https://techdocs.akamai.com/linode-api/reference/get-stack-scripts).   |

### metadata

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `user_data` | <center>`str`</center> | <center>Optional</center> | The user-defined data to supply for the Linode through the Metadata service.   |
| `user_data_encoded` | <center>`bool`</center> | <center>Optional</center> | Whether the user_data field content is already encoded in Base64.  **(Default: `False`)** |

### additional_ipv4

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `public` | <center>`bool`</center> | <center>**Required**</center> | Whether the allocated IPv4 address should be public or private.   |

### placement_group

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>**Required**</center> | The id of the placement group.   |
| `compliant_only` | <center>`bool`</center> | <center>Optional</center> | Whether the newly added/migrated/resized linode must be compliant for flexible placement groups.  **(Default: `False`)** |

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-config) for a list of returned fields


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
            "updated": "2018-01-01T00:01:01",
            "disk_encryption": "enabled"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-disk) for a list of returned fields


- `networking` - Networking information about this Linode Instance.

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


