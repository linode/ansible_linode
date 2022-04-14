.. _instance_module:


instance
========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Instances.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------


  **authorized_keys (type=list):**
    \• A list of SSH public key parts to deploy for the root user.


  **backup_id (type=int):**
    \• The id of the Backup to restore to the new Instance.

    \• May not be provided if “image” is given.


  **boot_config_label (type=str):**
    \• The label of the config to boot from.


  **booted (type=bool):**
    \• Whether the new Instance should be booted.

    \• This will default to True if the Instance is deployed from an Image or Backup.


  **configs (type=list):**
    \• A list of Instance configs to apply to the Linode.

    \• See https://www.linode.com/docs/api/linode-instances/#configuration-profile-create


      **comments (type=str):**
        \• Arbitrary User comments on this Config.


      **devices (type=dict):**
        \• The devices to map to this configuration.


          **sda (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.



          **sdb (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.



          **sdc (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.



          **sdd (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.



          **sde (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.



          **sdf (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.



          **sdg (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.



          **sdh (type=dict):**

              **disk_id (type=int):**
                \• The ID of the disk to attach to this Linode.


              **disk_label (type=str):**
                \• The label of the disk to attach to this Linode.


              **volume_id (type=int):**
                \• The ID of the volume to attach to this Linode.




      **helpers (type=dict):**
        \• Helpers enabled when booting to this Linode Config.


          **devtmpfs_automount (type=bool):**
            \• Populates the /dev directory early during boot without udev.


          **distro (type=bool):**
            \• Helps maintain correct inittab/upstart console device.


          **modules_dep (type=bool):**
            \• Creates a modules dependency file for the Kernel you run.


          **network (type=bool):**
            \• Automatically configures static networking.


          **updatedb_disabled (type=bool):**
            \• Disables updatedb cron job to avoid disk thrashing.



      **kernel (type=str):**
        \• A Kernel ID to boot a Linode with. Defaults to “linode/latest-64bit”          .


      **memory_limit (type=int):**
        \• Defaults to the total RAM of the Linode.


      **root_device (type=str):**
        \• The root device to boot.


      **run_level (type=str):**
        \• Defines the state of your Linode after booting.


      **virt_mode (type=str):**
        \• Controls the virtualization mode.

        \• Options: `paravirt`, `fullvirt`



  **disks (type=list):**
    \• A list of Disks to create on the Linode.

    \• See https://www.linode.com/docs/api/linode-instances/#disk-create


      **authorized_keys (type=list):**
        \• A list of SSH public key parts to deploy for the root user.


      **authorized_users (type=list):**
        \• A list of usernames.


      **filesystem (type=str):**
        \• The filesystem to create this disk with.


      **image (type=str):**
        \• An Image ID to deploy the Disk from.


      **root_pass (type=str):**
        \• The root user’s password on the newly-created Linode.


      **stackscript_data (type=dict):**
        \• An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance.

        \• Only valid when a stackscript_id is provided.

        \• See https://www.linode.com/docs/api/stackscripts/


      **stackscript_id (type=int):**
        \• The ID of the StackScript to use when creating the instance.

        \• See https://www.linode.com/docs/api/stackscripts/



  **group (type=str):**
    \• The group that the instance should be marked under.

    \• Please note, that group labelling is deprecated but still supported.

    \• The encouraged method for marking instances is to use tags.


  **image (type=str):**
    \• The image ID to deploy the instance disk from.


  **interfaces (type=list):**
    \• A list of network interfaces to apply to the Linode.

    \• See https://www.linode.com/docs/api/linode-instances/#linode-create__request-body-schema.


      **ipam_address (type=str):**
        \• This Network Interface’s private IP address in Classless           Inter-Domain Routing (CIDR) notation.


      **label (type=str):**
        \• The name of this interface.

        \• Required for vlan purpose interfaces.

        \• Must be an empty string or null for public purpose interfaces.



  **private_ip (type=bool):**
    \• If true, the created Linode will have private networking enabled.


  **region (type=str):**
    \• The location to deploy the instance in.

    \• See https://api.linode.com/v4/regions


  **root_pass (type=str):**
    \• The password for the root user.

    \• If not specified, one will be generated.

    \• This generated password will be available in the task success JSON.


  **stackscript_data (type=dict):**
    \• An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance.

    \• Only valid when a stackscript_id is provided.

    \• See https://www.linode.com/docs/api/stackscripts/.


  **stackscript_id (type=int):**
    \• The ID of the StackScript to use when creating the instance.

    \• See https://www.linode.com/docs/api/stackscripts/.


  **type (type=str):**
    \• The unique label to give this instance.


  **wait (type=bool, default=True):**
    \• Wait for the instance to have status `running` before returning.


  **wait_timeout (type=int, default=240):**
    \• The amount of time, in seconds, to wait for an instance to have status `running`.







Examples
--------

.. code-block:: yaml+jinja

    
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

    - name: Delete that new Linode instance.
      linode.cloud.instance:
        label: my-linode
        state: absent




Return Values
-------------

**instance (returned=always, type=dict):**

The instance description in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/linode-instances/#linode-view__responses>`_

Sample Response:

.. code-block:: JSON

    {
     "alerts": {
      "cpu": 90,
      "io": 10000,
      "network_in": 10,
      "network_out": 10,
      "transfer_quota": 80
     },
     "backups": {
      "enabled": false,
      "schedule": {
       "day": null,
       "window": null
      }
     },
     "created": "2018-09-26T08:12:33",
     "group": "app",
     "hypervisor": "kvm",
     "id": "xxxxxx",
     "image": "linode/ubuntu20.04",
     "ipv4": [
      "xxx.xxx.xxx.xxx"
     ],
     "ipv6": "xxxx:xxxx::xxxx:xxxx:xxxx:xxxx/64",
     "label": "my-linode",
     "region": "us-east",
     "root_pass": "foobar",
     "specs": {
      "disk": 25600,
      "memory": 1024,
      "transfer": 1000,
      "vcpus": 1
     },
     "status": "running",
     "tags": [
      "env=prod"
     ],
     "type": "g6-nanode-1",
     "updated": "2018-09-26T10:10:14",
     "watchdog_enabled": true
    }


**configs (returned=always, type=list):**

The configs tied to this Linode instance.

`Linode Response Object Documentation <https://www.linode.com/docs/api/linode-instances/#configuration-profile-view__responses>`_

Sample Response:

.. code-block:: JSON

    [
     {
      "comments": "",
      "created": "xxxxx",
      "devices": {
       "sda": null,
       "sdb": {
        "disk_id": "xxxxx",
        "volume_id": null
       },
       "sdc": null,
       "sdd": null,
       "sde": null,
       "sdf": null,
       "sdg": null,
       "sdh": null
      },
      "helpers": {
       "devtmpfs_automount": true,
       "distro": true,
       "modules_dep": true,
       "network": true,
       "updatedb_disabled": true
      },
      "id": "xxxxx",
      "initrd": null,
      "interfaces": [],
      "kernel": "linode/grub2",
      "label": "My Ubuntu 20.04 LTS Disk Profile",
      "memory_limit": 0,
      "root_device": "/dev/sda",
      "run_level": "default",
      "updated": "xxxxx",
      "virt_mode": "paravirt"
     }
    ]


**disks (returned=always, type=list):**

The disks tied to this Linode instance.

`Linode Response Object Documentation <https://www.linode.com/docs/api/linode-instances/#disk-view>`_

Sample Response:

.. code-block:: JSON

    [
     {
      "created": "xxxxx",
      "filesystem": "ext4",
      "id": "xxxxx",
      "label": "test-disk",
      "size": 10,
      "status": "ready",
      "updated": "xxxxx"
     }
    ]





Status
------




- This module is maintained by Linode.



Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)

