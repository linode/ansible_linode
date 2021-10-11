.. _firewall_info_module:


firewall_info
=============

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode Firewall.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **id (required=False, type=int, default=None):**
    \• The unique id of the Firewall.


  **label (required=False, type=str, default=None):**
    \• The Firewall’s label.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get info about a Firewall by label
      linode.cloud.firewall_info:
        label: 'my-firewall'

    - name: Get info about a Firewall by id
      linode.cloud.firewall_info:
        id: 12345




Return Values
-------------

**firewall (returned=always, type=dict):**

The Firewall description in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/networking/#firewall-view>`_

Sample Response:

.. code-block:: JSON

    {
     "created": "xxxxx",
     "id": "xxxx",
     "label": "my-firewall",
     "rules": {
      "inbound": [
       {
        "action": "ACCEPT",
        "addresses": {
         "ipv4": [
          "0.0.0.0/0"
         ],
         "ipv6": [
          "ff00::/8"
         ]
        },
        "description": "Allow inbound HTTP and HTTPS connections.",
        "label": "allow-http-in",
        "ports": "80,443",
        "protocol": "TCP"
       }
      ],
      "inbound_policy": "DROP",
      "outbound": [
       {
        "action": "ACCEPT",
        "addresses": {
         "ipv4": [
          "0.0.0.0/0"
         ],
         "ipv6": [
          "ff00::/8"
         ]
        },
        "description": "Allow outbound HTTP and HTTPS connections.",
        "label": "allow-http-out",
        "ports": "80,443",
        "protocol": "TCP"
       }
      ],
      "outbound_policy": "DROP"
     },
     "status": "enabled",
     "updated": "xxxxx"
    }


**devices (returned=always, type=list):**

A list of Firewall devices JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/networking/#firewall-device-view>`_

Sample Response:

.. code-block:: JSON

    [
     {
      "created": "xxxxxx",
      "entity": {
       "id": "xxxxxx",
       "label": "my-device",
       "type": "linode",
       "url": "/v4/linode/instances/xxxxxx"
      },
      "id": "xxxxxx",
      "updated": "xxxxxx"
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

