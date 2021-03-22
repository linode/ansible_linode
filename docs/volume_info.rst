.. _volume_info_module:


volume_info
===========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode volume.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 3.0



Parameters
----------

  label (optional, string, None)
    The Volume’s label.


  id (optional, int, None)
    The unique id of the volume.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get info about a volume by label
      linode.cloud.volume_info:
        label: example-volume
        
    - name: Get info about a volume by id
      linode.cloud.volume_info:
        id: 12345



Return Values
-------------

volume (always, dict, {
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

