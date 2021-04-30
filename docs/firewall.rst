.. _firewall_module:


firewall
========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Firewalls. This endpoint is currently in beta and will only function correctly if `api_version` is set to `v4beta`.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 5.1.0



Parameters
----------

  label (True, str, None)
    The unique label to give this Firewall.


  status (optional, str, None)
    The status of this Firewall.


  devices (optional, list, None)
    The devices that are attached to this Firewall.


    id (True, str, None)
      The unique ID of the device to attach to this Firewall.


    type (optional, str, linode)
      The type of device to be attached to this Firewall.



  rules (optional, dict, None)
    The inbound and outbound access rules to apply to the Firewall.


    inbound_policy (True, str, None)
      The default behavior for inbound traffic.


    outbound_policy (True, str, None)
      The default behavior for outbound traffic.


    inbound (optional, list, None)
      A list of rules for inbound traffic.


      label (True, str, None)
        The label of this rule.


      action (True, str, None)
        Controls whether traffic is accepted or dropped by this rule.


      description (optional, str, None)
        The description of this rule.


      addresses (optional, list, None)
        Allowed IPv4 or IPv6 addresses.


        ipv4 (optional, list, None)
          A list of IPv4 addresses or networks.

          Must be in IP/mask format.


        ipv6 (optional, list, None)
          A list of IPv4 addresses or networks.

          Must be in IP/mask format.




    outbound (optional, list, None)
      A list of rules for outbound traffic.


      label (True, str, None)
        The label of this rule.


      action (True, str, None)
        Controls whether traffic is accepted or dropped by this rule.


      description (optional, str, None)
        The description of this rule.


      addresses (optional, list, None)
        Allowed IPv4 or IPv6 addresses.


        ipv4 (optional, list, None)
          A list of IPv4 addresses or networks.

          Must be in IP/mask format.


        ipv6 (optional, list, None)
          A list of IPv4 addresses or networks.

          Must be in IP/mask format.












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

**firewall (always, dict):**

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


**devices (always, list):**

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

