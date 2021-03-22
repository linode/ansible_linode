.. _nodebalancer_module:


nodebalancer
============

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode NodeBalancers.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 3.0



Parameters
----------

  label (True, string, None)
    The unique label to give this NodeBalancer


  region (True, str, None)
    The location to deploy the instance in.

    See https://api.linode.com/v4/regions


  configs (False, list, None)
    A list of configs to be added to the NodeBalancer.


    algorithm (optional, str, None)
      What algorithm this NodeBalancer should use for routing traffic to backends.


    check (optional, str, None)
      The type of check to perform against backends to ensure they are serving requests.

      This is used to determine if backends are up or down.


    check_attempts (optional, int, None)
      How many times to attempt a check before considering a backend to be down.


    check_body (optional, str, None)
      This value must be present in the response body of the check in order for it to pass.

      If this value is not present in the response body of a check request, the backend is considered to be down.


    check_interval (optional, int, None)
      How often, in seconds, to check that backends are up and serving requests.


    check_passive (optional, bool, None)
      If true, any response from this backend with a 5xx status code will be enough for it to be considered unhealthy and taken out of rotation.


    check_path (optional, str, None)
      The URL path to check on each backend. If the backend does not respond to this request it is considered to be down.


    check_timeout (optional, int, None)
      How long, in seconds, to wait for a check attempt before considering it failed.


    cipher_suite (optional, str, recommended)
      What ciphers to use for SSL connections served by this NodeBalancer.

      ``legacy`` is considered insecure and should only be used if necessary.


    port (optional, int, None)
      The port for the Config to listen on.


    protocol (optional, str, None)
      The protocol this port is configured to serve.


    proxy_protocol (optional, str, None)
      ProxyProtocol is a TCP extension that sends initial TCP connection information such as source/destination IPs and ports to backend devices.


    ssl_cert (optional, str, None)
      The PEM-formatted public SSL certificate (or the combined PEM-formatted SSL certificate and Certificate Authority chain) that should be served on this NodeBalancerConfig’s port.


    ssl_key (optional, str, None)
      The PEM-formatted private key for the SSL certificate set in the ssl_cert field.


    stickiness (optional, str, None)
      Controls how session stickiness is handled on this port.


    nodes (optional, list, None)
      A list of Nodes to be created with the parent Config.


      label (True, str, None)
        The label to give to this Node.


      address (True, str, None)
        The private IP Address where this backend can be reached.


      mode (optional, str, None)
        The mode this NodeBalancer should use when sending traffic to this backend.


      weight (optional, int, None)
        Nodes with a higher weight will receive more traffic.











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

nodebalancer (always, dict):
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
  The NodeBalancer in JSON serialized form.


configs (always, list):
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
  A list of configs applied to the NodeBalancer.


nodes (always, list):
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
  A list of all nodes associated with the NodeBalancer.





Status
------




- This module is maintained by Linode.



Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)

