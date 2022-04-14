.. _object_keys_module:


object_keys
===========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Object Storage Keys.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------


  **access (type=list):**
    \• A list of access permissions to give the key.



  **label (type=str):**
    \• The unique label to give this key.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create an Object Storage key
      linode.cloud.object_keys:
        label: 'my-fullaccess-key'
        state: present
        
    - name: Create a limited Object Storage key
      linode.cloud.object_keys:
        label: 'my-limited-key'
        access:
          - cluster: us-east-1
            bucket_name: my-bucket
            permissions: read_write
        state: present
        
    - name: Remove an object storage key
      linode.cloud.object_keys:
        label: 'my-key'
        state: absent




Return Values
-------------

**key (returned=always, type=dict):**

The Object Storage key in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/object-storage/#object-storage-key-view__responses>`_

Sample Response:

.. code-block:: JSON

    {
     "access_key": "xxxxxxxxxxxxxxxxx",
     "bucket_access": [
      {
       "bucket_name": "my-bucket",
       "cluster": "us-east-1",
       "permissions": "read_write"
      }
     ],
     "id": "xxxxx",
     "label": "my-key",
     "limited": true,
     "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
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
- Jacob Riddle (@jriddle)

