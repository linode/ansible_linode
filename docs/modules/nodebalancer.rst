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

  **client_conn_throttle (required=False, type=int, default=None):**
    \• Throttle connections per second.

    \• Set to 0 (zero) to disable throttling.


  **configs (required=False, type=list, default=None):**
    \• A list of configs to apply to the NodeBalancer.


      **algorithm (required=False, type=str, default=None):**
        \• What algorithm this NodeBalancer should use for routing traffic to backends.


      **check (required=False, type=str, default=None):**
        \• The type of check to perform against backends to ensure they are serving requests.


      **check_attempts (required=False, type=int, default=None):**
        \• How many times to attempt a check before considering a backend to be down.


      **check_body (required=False, type=str, default=):**
        \• This value must be present in the response body of the check in order for it to pass.

        \• If this value is not present in the response body of a check request, the backend is considered to be down.


      **check_interval (required=False, type=int, default=None):**
        \• How often, in seconds, to check that backends are up and serving requests.


      **check_passive (required=False, type=bool, default=None):**
        \• If true, any response from this backend with a 5xx status code will be enough for it to be considered unhealthy and taken out of rotation.


      **check_path (required=False, type=str, default=None):**
        \• The URL path to check on each backend. If the backend does not respond to this request it is considered to be down.


      **check_timeout (required=False, type=int, default=None):**
        \• How long, in seconds, to wait for a check attempt before considering it failed.


      **cipher_suite (required=False, type=str, default=recommended):**
        \• What ciphers to use for SSL connections served by this NodeBalancer.


      **nodes (required=False, type=list, default=None):**
        \• A list of nodes to apply to this config.


          **address (required=True, type=str, default=None):**
            \• The private IP Address where this backend can be reached.

            \• This must be a private IP address.


          **label (required=True, type=str, default=None):**
            \• The label for this node.


          **mode (required=False, type=str, default=None):**
            \• The mode this NodeBalancer should use when sending traffic to this backend.


          **weight (required=False, type=int, default=None):**
            \• Nodes with a higher weight will receive more traffic.



      **port (required=False, type=int, default=None):**
        \• The port this Config is for.


      **protocol (required=False, type=str, default=None):**
        \• The protocol this port is configured to serve.


      **proxy_protocol (required=False, type=str, default=None):**
        \• ProxyProtocol is a TCP extension that sends initial TCP connection information such as source/destination IPs and ports to backend devices.


      **ssl_cert (required=False, type=str, default=None):**
        \• The PEM-formatted public SSL certificate (or the combined PEM-formatted           SSL certificate and Certificate Authority chain) that should be served           on this NodeBalancerConfig’s port.


      **ssl_key (required=False, type=str, default=None):**
        \• The PEM-formatted private key for the SSL certificate set in the ssl_cert field.


      **stickiness (required=False, type=str, default=None):**
        \• Controls how session stickiness is handled on this port.



  **label (required=False, type=str, default=None):**
    \• The unique label to give this NodeBalancer.


  **region (required=False, type=str, default=None):**
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

**nodebalancer (returned=always, type=dict):**

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

