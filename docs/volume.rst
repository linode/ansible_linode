.. _volume_module:


volume
======

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode volumes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 3.0



Parameters
----------

  label (True, string, None)
    The Volume’s label, which is also used in the filesystem_path of the resulting volume.


  region (optional, str, None)
    The location to deploy the volume in.

    See https://api.linode.com/v4/regions


  size (optional, int, None)
    The size of this volume, in GB.

    Be aware that volumes may only be resized up after creation.


  linode_id (optional, int, None)
    The Linode this volume should be attached to upon creation.

    If not given, the volume will be created without an attachment.


  config_id (optional, int, None)
    When creating a Volume attached to a Linode, the ID of the Linode Config to include the new Volume in.


  attached (optional, bool, None)
    If true, the volume will be attached to a Linode. Otherwise, the volume will be detached.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a volume attached to an instance
      linode.cloud.volume:
        label: example-volume
        region: us-east
        size: 30
        linode_id: 12345
        state: present
        
    - name: Create an unattached volume
      linode.cloud.volume:
        label: example-volume
        region: us-east
        size: 30
        state: present
        
    - name: Resize a volume
      linode.cloud.volume:
        label: example-volume
        size: 50
        state: present
        
    - name: Detach a volume
      linode.cloud.volume:
        label: example-volume
        attached: false
        state: present
        
    - name: Delete a volume
      linode.cloud.volume:
        label: example-volume
        state: absent



Return Values
-------------

volume (always, dict, .. code-block:: json {
 "created": "",
 "filesystem_path": "/dev/disk/by-id/xxxxxx",
 "id": "xxxxxx",
 "label": "xxxxxx",
 "linode_id": "xxxxxx",
 "linode_label": "xxxxxx",
 "region": "us-east",
 "size": 30,
 "status": "creating",
 "tags": [],
 "updated": "2021-03-05T19:05:33"
})
  The volume in JSON serialized form.





Status
------




- This module is maintained by Linode.



Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)

