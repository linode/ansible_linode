.. _nodebalancer_module:


nodebalancer
============

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage a Linode NodeBalancer.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **label (Required, type=str):**
    \• The unique label to give this NodeBalancer.



  **client_conn_throttle (type=int):**
    \• Throttle connections per second.

    \• Set to 0 (zero) to disable throttling.


  **configs (type=list):**
    \• A list of configs to apply to the NodeBalancer.


      **algorithm (type=str):**
        \• What algorithm this NodeBalancer should use for routing traffic to backends.

        \• Options: `roundrobin`, `leastconn`, `source`


      **check (type=str):**
        \• The type of check to perform against backends to ensure they are serving requests.

        \• Options: `none`, `connection`, `http`, `http_body`


      **check_attempts (type=int):**
        \• How many times to attempt a check before considering a backend to be down.


      **check_body (type=str):**
        \• This value must be present in the response body of the check in order for it to pass.

        \• If this value is not present in the response body of a check request, the backend is considered to be down.


      **check_interval (type=int):**
        \• How often, in seconds, to check that backends are up and serving requests.


      **check_passive (type=bool):**
        \• If true, any response from this backend with a 5xx status code will be enough for it to be considered unhealthy and taken out of rotation.


      **check_path (type=str):**
        \• The URL path to check on each backend. If the backend does not respond to this request it is considered to be down.


      **check_timeout (type=int):**
        \• How long, in seconds, to wait for a check attempt before considering it failed.


      **cipher_suite (type=str, default=recommended):**
        \• What ciphers to use for SSL connections served by this NodeBalancer.

        \• Options: `recommended`, `legacy`


      **nodes (type=list):**
        \• A list of nodes to apply to this config. These can alternatively be configured through the nodebalancer_node module.


          **mode (type=str):**
            \• The mode this NodeBalancer should use when sending traffic to this backend.

            \• Options: `accept`, `reject`, `drain`, `backup`


          **weight (type=int):**
            \• Nodes with a higher weight will receive more traffic.



      **port (type=int):**
        \• The port this Config is for.


      **protocol (type=str):**
        \• The protocol this port is configured to serve.

        \• Options: `http`, `https`, `tcp`


      **proxy_protocol (type=str):**
        \• ProxyProtocol is a TCP extension that sends initial TCP connection information such as source/destination IPs and ports to backend devices.

        \• Options: `none`, `v1`, `v2`


      **ssl_cert (type=str):**
        \• The PEM-formatted public SSL certificate (or the combined PEM-formatted           SSL certificate and Certificate Authority chain) that should be served           on this NodeBalancerConfig’s port.


      **ssl_key (type=str):**
        \• The PEM-formatted private key for the SSL certificate set in the ssl_cert field.


      **stickiness (type=str):**
        \• Controls how session stickiness is handled on this port.

        \• Options: `none`, `table`, `http_cookie`



  **region (type=str):**
    \• The ID of the Region to create this NodeBalancer in.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a Linode NodeBalancer
      linode.cloud.nodebalancer:
        label: my-loadbalancer
        region: us-east
        tags: [ prod-env ]
        state: present
        configs:
          - port: 80
            protocol: http
            algorithm: roundrobin
            nodes:
              - label: node1
                address: 0.0.0.0:80

    - name: Delete the NodeBalancer
      linode.cloud.nodebalancer:
        label: my-loadbalancer
        region: us-east
        state: absent




Return Values
-------------

**node_balancer (returned=always, type=dict):**

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


**configs (returned=always, type=list):**

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


**nodes (returned=always, type=list):**

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

