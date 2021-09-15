.. _nodebalancer_info_module:


nodebalancer_info
=================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode NodeBalancer.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.0



Parameters
----------

  id (False, int, None)
    The ID of this NodeBalancer.


  label (False, str, None)
    The label of this NodeBalancer.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get a NodeBalancer by its id
      linode.cloud.nodebalancer_info:
        id: 12345
        
    - name: Get a NodeBalancer by its label
      linode.cloud.nodebalancer_info:
        label: cool_nodebalancer




Return Values
-------------

**nodebalancer (always, dict):**

The NodeBalancer in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/nodebalancers/#nodebalancer-view__responses>`_

Sample Response:

.. code-block:: JSON

    {
     "client_conn_throttle": 0,
     "created": "",
     "hostname": "xxxx.newark.nodebalancer.linode.com",
     "id": "xxxxxx",
     "ipv4": "xxx.xxx.xxx.xxx",
     "ipv6": "xxxx:xxxx::xxxx:xxxx:xxxx:xxxx",
     "label": "my-loadbalancer",
     "region": "us-east",
     "tags": [],
     "transfer": {
      "in": 0,
      "out": 0,
      "total": 0
     },
     "updated": ""
    }


**configs (always, list):**

A list of configs applied to the NodeBalancer.

`Linode Response Object Documentation <https://www.linode.com/docs/api/nodebalancers/#config-view__responses>`_

Sample Response:

.. code-block:: JSON

    [
     {
      "algorithm": "roundrobin",
      "check": "none",
      "check_attempts": 3,
      "check_body": "",
      "check_interval": 0,
      "check_passive": true,
      "check_path": "",
      "check_timeout": 30,
      "cipher_suite": "recommended",
      "id": "xxxxxx",
      "nodebalancer_id": "xxxxxx",
      "nodes_status": {
       "down": 1,
       "up": 0
      },
      "port": 80,
      "protocol": "http",
      "proxy_protocol": "none",
      "ssl_cert": null,
      "ssl_commonname": "",
      "ssl_fingerprint": "",
      "ssl_key": null,
      "stickiness": "none"
     }
    ]


**nodes (always, list):**

A list of all nodes associated with the NodeBalancer.

`Linode Response Object Documentation <https://www.linode.com/docs/api/nodebalancers/#node-view__responses>`_

Sample Response:

.. code-block:: JSON

    [
     {
      "address": "xxx.xxx.xxx.xx:80",
      "config_id": "xxxxxx",
      "id": "xxxxxx",
      "label": "node1",
      "mode": "accept",
      "nodebalancer_id": "xxxxxx",
      "status": "Unknown",
      "weight": 1
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

