# instance

Manage Linode Instances, Configs, and Disks.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
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
    state: present
```

```yaml
- name: Delete a Linode instance.
  linode.cloud.instance:
    label: my-linode
    state: absent
```


## Parameters



- `state` (`str`) - **(Required)** The desired state of the target.  (Choices:  `present` `absent`)
- `type` (`str`) -  The unique label to give this instance.  
- `region` (`str`) -  The location to deploy the instance in. See the [Linode API documentation](https://api.linode.com/v4/regions).  
- `image` (`str`) -  The image ID to deploy the instance disk from.  
- `authorized_keys` (`list`) -  A list of SSH public key parts to deploy for the root user.  
- `root_pass` (`str`) -  The password for the root user. If not specified, one will be generated. This generated password will be available in the task success JSON.  
- `stackscript_id` (`int`) -  The ID of the StackScript to use when creating the instance. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).  
- `stackscript_data` (`dict`) -  An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance. Only valid when a stackscript_id is provided. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).  
- `private_ip` (`bool`) -  If true, the created Linode will have private networking enabled.  
- `group` (`str`) -  The group that the instance should be marked under. Please note, that group labelling is deprecated but still supported. The encouraged method for marking instances is to use tags.  
- `boot_config_label` (`str`) -  The label of the config to boot from.  
- `configs` (`list`) -  A list of Instance configs to apply to the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#configuration-profile-create).  
    - `label` (`str`) - **(Required)** The label to assign to this config.  
    - `comments` (`str`) -  Arbitrary User comments on this Config.  
    - `devices` (`dict`) -  The devices to map to this configuration.  
        - `sda` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
        - `sdb` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
        - `sdc` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
        - `sdd` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
        - `sde` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
        - `sdf` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
        - `sdg` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
        - `sdh` (`dict`)
            - `disk_label` (`str`) -  The label of the disk to attach to this Linode.  
            - `disk_id` (`int`) -  The ID of the disk to attach to this Linode.  
            - `volume_id` (`int`) -  The ID of the volume to attach to this Linode.  
    - `helpers` (`dict`) -  Helpers enabled when booting to this Linode Config.  
        - `devtmpfs_automount` (`bool`) -  Populates the /dev directory early during boot without udev.  
        - `distro` (`bool`) -  Helps maintain correct inittab/upstart console device.  
        - `modules_dep` (`bool`) -  Creates a modules dependency file for the Kernel you run.  
        - `network` (`bool`) -  Automatically configures static networking.  
        - `updatedb_disabled` (`bool`) -  Disables updatedb cron job to avoid disk thrashing.  
    - `kernel` (`str`) -  A Kernel ID to boot a Linode with. Defaults to “linode/latest-64bit”.  
    - `memory_limit` (`int`) -  Defaults to the total RAM of the Linode.  
    - `root_device` (`str`) -  The root device to boot.  
    - `run_level` (`str`) -  Defines the state of your Linode after booting.  
    - `virt_mode` (`str`) -  Controls the virtualization mode.  (Choices:  `paravirt` `fullvirt`)
- `disks` (`list`) -  A list of Disks to create on the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#disk-create).  
    - `label` (`str`) - **(Required)** The label to give this Disk.  
    - `size` (`int`) - **(Required)** The size of the Disk in MB.  
    - `authorized_keys` (`list`) -  A list of SSH public key parts to deploy for the root user.  
    - `authorized_users` (`list`) -  A list of usernames.  
    - `filesystem` (`str`) -  The filesystem to create this disk with.  
    - `image` (`str`) -  An Image ID to deploy the Disk from.  
    - `root_pass` (`str`) -  The root user’s password on the newly-created Linode.  
    - `stackscript_id` (`int`) -  The ID of the StackScript to use when creating the instance. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).  
    - `stackscript_data` (`dict`) -  An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance. Only valid when a stackscript_id is provided. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).  
- `interfaces` (`list`) -  A list of network interfaces to apply to the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#linode-create__request-body-schema).  
    - `purpose` (`str`) - **(Required)** The type of interface.  (Choices:  `public` `vlan`)
    - `label` (`str`) -  The name of this interface. Required for vlan purpose interfaces. Must be an empty string or null for public purpose interfaces.  
    - `ipam_address` (`str`) -  This Network Interface’s private IP address in Classless Inter-Domain Routing (CIDR) notation.  
- `booted` (`bool`) -  Whether the new Instance should be booted. This will default to True if the Instance is deployed from an Image or Backup.  
- `backup_id` (`int`) -  The id of the Backup to restore to the new Instance. May not be provided if “image” is given.  
- `wait` (`bool`) -  Wait for the instance to have status `running` before returning.  ( Default: `True`)
- `wait_timeout` (`int`) -  The amount of time, in seconds, to wait for an instance to have status `running`.  ( Default: `240`)


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


