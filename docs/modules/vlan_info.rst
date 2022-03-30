.. _vlan_info_module:


vlan_info
=========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode VLAN.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **label (Required, type=str):**
    \• The VLAN’s label.








Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get info about a VLAN by label
      linode.cloud.vlan_info:
        label: example-vlan




Return Values
-------------

**vlan (returned=always, type=dict):**

The VLAN in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/networking/#vlans-list__response-samples>`_

Sample Response:

.. code-block:: JSON

    {
     "created": "xxxxx",
     "label": "example-vlan",
     "linodes": [
      12345
     ],
     "region": "us-southeast"
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

