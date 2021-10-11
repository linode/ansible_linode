.. _volume_info_module:


volume_info
===========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode Volume.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **id (required=False, type=int, default=None):**
    \• The ID of the Volume.


  **label (required=False, type=str, default=None):**
    \• The label of the Volume.







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

**volume (returned=always, type=dict):**

The volume in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/volumes/#volume-view__responses>`_

Sample Response:

.. code-block:: JSON

    {
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
    }





Status
------




- This module is maintained by Linode.



Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)

