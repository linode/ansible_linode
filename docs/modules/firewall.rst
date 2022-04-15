.. _firewall_module:


firewall
========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Firewalls.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------


  **devices (type=list):**
    \• The devices that are attached to this Firewall.


      **type (type=str, default=linode):**
        \• The type of device to be attached to this Firewall.



  **label (type=str):**
    \• The unique label to give this Firewall.


  **rules (type=dict):**
    \• The inbound and outbound access rules to apply to this Firewall.


      **inbound (type=list):**
        \• A list of rules for inbound traffic.


          **addresses (type=dict):**
            \• Allowed IPv4 or IPv6 addresses.


              **ipv4 (type=list):**
                \• A list of IPv4 addresses or networks.

                \• Must be in IP/mask format.


              **ipv6 (type=list):**
                \• A list of IPv4 addresses or networks.

                \• Must be in IP/mask format.



          **description (type=str):**
            \• A description for this rule.


          **ports (type=str):**
            \• A string representing the port or ports on which traffic will be allowed.

            \• See https://www.linode.com/docs/api/networking/#firewall-create


          **protocol (type=str):**
            \• The type of network traffic to allow.



      **inbound_policy (type=str):**
        \• The default behavior for inbound traffic.


      **outbound (type=list):**
        \• A list of rules for outbound traffic.


          **addresses (type=dict):**
            \• Allowed IPv4 or IPv6 addresses.


              **ipv4 (type=list):**
                \• A list of IPv4 addresses or networks.

                \• Must be in IP/mask format.


              **ipv6 (type=list):**
                \• A list of IPv4 addresses or networks.

                \• Must be in IP/mask format.



          **description (type=str):**
            \• A description for this rule.


          **ports (type=str):**
            \• A string representing the port or ports on which traffic will be allowed.

            \• See https://www.linode.com/docs/api/networking/#firewall-create


          **protocol (type=str):**
            \• The type of network traffic to allow.



      **outbound_policy (type=str):**
        \• The default behavior for outbound traffic.



  **status (type=str):**
    \• The status of this Firewall.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a Linode Firewall
      linode.cloud.firewall:
        api_version: v4beta
        label: 'my-firewall'
        devices:
          - id: 123
            type: linode
        rules:
          inbound_policy: DROP
          inbound:
            - label: allow-http-in
              addresses:
                ipv4:
                  - 0.0.0.0/0
                ipv6:
                  - 'ff00::/8'
              description: Allow inbound HTTP and HTTPS connections.
              ports: '80,443'
              protocol: TCP
              action: ACCEPT

          outbound_policy: DROP
          outbound:
            - label: allow-http-out
              addresses:
                ipv4:
                  - 0.0.0.0/0
                ipv6:
                  - 'ff00::/8'
              description: Allow outbound HTTP and HTTPS connections.
              ports: '80,443'
              protocol: TCP
              action: ACCEPT
        state: present
        
    - name: Delete a Linode Firewall
      linode.cloud.firewall:
        api_version: v4beta
        label: 'my-firewall'
        state: absent




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
- Jacob Riddle (@jriddle)

