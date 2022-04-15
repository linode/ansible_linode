.. _firewall_device_module:


firewall_device
===============

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Firewall Devices.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **entity_id (Required, type=int):**
    \• The ID for this Firewall Device. This will be the ID of the Linode Entity.


  **entity_type (Required, type=str):**
    \• The type of Linode Entity. Currently only supports linode.

    \• Options: `linode`


  **firewall_id (Required, type=int):**
    \• The ID of the Firewall that contains this device.








Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a Firewall
      linode.cloud.firewall:
        label: my-firewall
        rules:
          inbound_policy: DROP
        state: present
      register: firewall_result

    - name: Create an Instance
      linode.cloud.instance:
        label: my-instance
        region: us-east
        private_ip: true
        type: g6-standard-1
        state: present
      register: instance_result

    - name: Attach the instance to the Firewall
      linode.cloud.firewall_device:
        firewall_id: '{{ firewall_result.firewall.id }}'
        entity_id: '{{ instance_result.instance.id }}'
        entity_type: 'linode'
        state: present




Return Values
-------------

**device (returned=always, type=dict):**

The Firewall Device in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/networking/#firewall-device-view__response-samples>`_

Sample Response:

.. code-block:: JSON

    {
     "created": "2018-01-01T00:01:01",
     "entity": {
      "id": 123,
      "label": "my-linode",
      "type": "linode",
      "url": "/v4/linode/instances/123"
     },
     "id": 123,
     "updated": "2018-01-02T00:01:01"
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

