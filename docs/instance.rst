.. _instance_module:


instance
========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode instances.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 3.0



Parameters
----------

  label (True, string, None)
    The unique label to give this instance.


  type (optional, any, None)
    The type or plan of this instance.

    See https://api.linode.com/v4/linode/types


  region (True, str, None)
    The location to deploy the instance in.

    See https://api.linode.com/v4/regions


  image (True, str, None)
    The image ID to deploy the instance disk from.


  group (False, str, None)
    The group that the instance should be marked under. Please note, that group labelling is deprecated but still supported. The encouraged method for marking instances is to use tags.


  tags (False, list, None)
    The tags that the instance should be marked under.

    See https://www.linode.com/docs/api/tags/.


  root_pass (False, str, None)
    The password for the root user. If not specified, one will be generated. This generated password will be available in the task success JSON.


  private_ip (False, bool, None)
    If true, the created Linode will have private networking enabled.


  authorized_keys (False, list, None)
    A list of SSH public key parts to deploy for the root user.


  stackscript_id (False, int, None)
    The ID of the StackScript to use when creating the instance. See https://www.linode.com/docs/api/stackscripts/.


  stackscript_data (False, dict, None)
    An object containing arguments to any User Defined Fields present in the StackScript used when creating the instance. Only valid when a stackscript_id is provided. See https://www.linode.com/docs/api/stackscripts/.


  interfaces (optional, list, None)
    A list of network interfaces to apply to the Linode.

    VLANs are currently in beta and will only function correctly if `api_version` is set to `v4beta`.

    See https://www.linode.com/docs/api/linode-instances/#linode-create__request-body-schema.


    purpose (True, str, None)
      The type of interface.


    label (optional, str, None)
      The name of this interface.

      Required for vlan purpose interfaces.

      Must be an empty string or null for public purpose interfaces.


    ipam_address (optional, str, None)
      This Network Interface’s private IP address in Classless Inter-Domain Routing (CIDR) notation.



  booted (optional, any, None)
    Whether the new Instance should be booted. This will default to True if the Instance is deployed from an Image or Backup.


  backup_id (optional, any, None)
    The id of the Backup to restore to the new Instance. May not be provided if “image” is given.


  wait (optional, bool, True)
    Wait for the instance to have status `running` before returning.


  wait_timeout (optional, int, 240)
    The amount of time, in seconds, to wait for an instance to have status `running`.


  state (optional, str, None)
    The desired instance state.









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

**instance (always, dict):**

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


**configs (always, list):**

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





Status
------




- This module is maintained by Linode.



Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)

