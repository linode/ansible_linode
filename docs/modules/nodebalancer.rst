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

- python >= 3.0



Parameters
----------

  client_conn_throttle (False, int, None)
    Throttle connections per second.

    Set to 0 (zero) to disable throttling.


  configs (False, list, None)
    A list of configs to apply to the NodeBalancer.


      algorithm (False, str, None)
        What algorithm this NodeBalancer should use for routing traffic to backends.


      check (False, str, None)
        The type of check to perform against backends to ensure they are serving requests.


      check_attempts (False, int, None)
        How many times to attempt a check before considering a backend to be down.


      check_body (False, str, )
        This value must be present in the response body of the check in order for it to pass.

        If this value is not present in the response body of a check request, the backend is considered to be down.


      check_interval (False, int, None)
        How often, in seconds, to check that backends are up and serving requests.


      check_passive (False, bool, None)
        If true, any response from this backend with a 5xx status code will be enough for it to be considered unhealthy and taken out of rotation.


      check_path (False, str, None)
        The URL path to check on each backend. If the backend does not respond to this request it is considered to be down.


      check_timeout (False, int, None)
        How long, in seconds, to wait for a check attempt before considering it failed.


      cipher_suite (False, str, recommended)
        What ciphers to use for SSL connections served by this NodeBalancer.


      nodes (False, list, None)
        A list of nodes to apply to this config.


          address (True, str, None)
            The private IP Address where this backend can be reached.

            This must be a private IP address.


          label (True, str, None)
            The label for this node.


          mode (False, str, None)
            The mode this NodeBalancer should use when sending traffic to this backend.


          weight (False, int, None)
            Nodes with a higher weight will receive more traffic.



      port (False, int, None)
        The port this Config is for.


      protocol (False, str, None)
        The protocol this port is configured to serve.


      proxy_protocol (False, str, None)
        ProxyProtocol is a TCP extension that sends initial TCP connection information such as source/destination IPs and ports to backend devices.


      ssl_cert (False, str, None)
        The PEM-formatted public SSL certificate (or the combined PEM-formatted           SSL certificate and Certificate Authority chain) that should be served           on this NodeBalancerConfig’s port.


      ssl_key (False, str, None)
        The PEM-formatted private key for the SSL certificate set in the ssl_cert field.


      stickiness (False, str, None)
        Controls how session stickiness is handled on this port.



  label (False, str, None)
    The unique label to give this NodeBalancer.


  region (False, str, None)
    The ID of the Region to create this NodeBalancer in.









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

