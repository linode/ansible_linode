# instance

Manage Linode Instances, Configs, and Disks.


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


- `type` -  The unique label to give this instance. 
- `region` -  The location to deploy the instance in. See the [Linode API documentation](https://api.linode.com/v4/regions). 
- `image` -  The image ID to deploy the instance disk from. 
- `authorized_keys` -  A list of SSH public key parts to deploy for the root user. 
- `root_pass` -  The password for the root user. If not specified, one will be generated. This generated password will be available in the task success JSON. 
- `stackscript_id` -  The ID of the StackScript to use when creating the instance. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/). 
- `stackscript_data` -  An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance. Only valid when a stackscript_id is provided. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/). 
- `private_ip` -  If true, the created Linode will have private networking enabled. 
- `group` -  The group that the instance should be marked under. Please note, that group labelling is deprecated but still supported. The encouraged method for marking instances is to use tags. 
- `boot_config_label` -  The label of the config to boot from. 
- `configs` -  A list of Instance configs to apply to the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#configuration-profile-create). 
    - `comments` -  Arbitrary User comments on this Config. 
    - `devices` -  The devices to map to this configuration. 
        - `sda`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
        - `sdb`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
        - `sdc`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
        - `sdd`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
        - `sde`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
        - `sdf`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
        - `sdg`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
        - `sdh`
            - `disk_label` -  The label of the disk to attach to this Linode. 
            - `disk_id` -  The ID of the disk to attach to this Linode. 
            - `volume_id` -  The ID of the volume to attach to this Linode. 
    - `helpers` -  Helpers enabled when booting to this Linode Config. 
        - `devtmpfs_automount` -  Populates the /dev directory early during boot without udev. 
        - `distro` -  Helps maintain correct inittab/upstart console device. 
        - `modules_dep` -  Creates a modules dependency file for the Kernel you run. 
        - `network` -  Automatically configures static networking. 
        - `updatedb_disabled` -  Disables updatedb cron job to avoid disk thrashing. 
    - `kernel` -  A Kernel ID to boot a Linode with. Defaults to “linode/latest-64bit”. 
    - `label` - **(Required)** The label to assign to this config. 
    - `memory_limit` -  Defaults to the total RAM of the Linode. 
    - `root_device` -  The root device to boot. 
    - `run_level` -  Defines the state of your Linode after booting. 
    - `virt_mode` -  Controls the virtualization mode. 
- `disks` -  A list of Disks to create on the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#disk-create). 
    - `authorized_keys` -  A list of SSH public key parts to deploy for the root user. 
    - `authorized_users` -  A list of usernames. 
    - `filesystem` -  The filesystem to create this disk with. 
    - `image` -  An Image ID to deploy the Disk from. 
    - `label` - **(Required)** The label to give this Disk. 
    - `root_pass` -  The root user’s password on the newly-created Linode. 
    - `size` - **(Required)** The size of the Disk in MB. 
    - `stackscript_id` -  The ID of the StackScript to use when creating the instance. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/). 
    - `stackscript_data` -  An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance. Only valid when a stackscript_id is provided. See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/). 
- `interfaces` -  A list of network interfaces to apply to the Linode. See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/#linode-create__request-body-schema). 
    - `purpose` - **(Required)** The type of interface. 
    - `label` -  The name of this interface. Required for vlan purpose interfaces. Must be an empty string or null for public purpose interfaces. 
    - `ipam_address` -  This Network Interface’s private IP address in Classless Inter-Domain Routing (CIDR) notation. 
- `booted` -  Whether the new Instance should be booted. This will default to True if the Instance is deployed from an Image or Backup. 
- `backup_id` -  The id of the Backup to restore to the new Instance. May not be provided if “image” is given. 
- `wait` -  Wait for the instance to have status `running` before returning. 
- `wait_timeout` -  The amount of time, in seconds, to wait for an instance to have status `running`. 


## Return Values

- `instance` - The instance description in JSON serialized form.
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-instances/#linode-view__responses) for a list of returned fields
- `configs` - A list of configs tied to this Linode Instance.
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-instances/#configuration-profile-view__responses) for a list of returned fields
- `disks` - A list of disks tied to this Linode Instance.
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-instances/#disk-view) for a list of returned fields
