.. _nodebalancer_info_module:


nodebalancer_info
=================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a NodeBalancer.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 3.0



Parameters
----------

  label (optional, string, None)
    The label of this NodeBalancer


  id (optional, int, None)
    The unique id of this NodeBalancer









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

nodebalancer (Always., dict, {'changed': False, 'configs': [{'algorithm': 'roundrobin', 'check': 'none', 'check_attempts': 3, 'check_body': '', 'check_interval': 0, 'check_passive': True, 'check_path': '', 'check_timeout': 30, 'cipher_suite': 'recommended', 'id': 'xxxxx', 'nodebalancer_id': 'xxxxxx', 'nodes_status': {'down': 1, 'up': 0}, 'port': 80, 'protocol': 'http', 'proxy_protocol': 'none', 'ssl_cert': None, 'ssl_commonname': '', 'ssl_fingerprint': '', 'ssl_key': None, 'stickiness': 'none'}], 'node_balancer': {'client_conn_throttle': 0, 'created': '2021-03-03T17:45:37', 'hostname': 'xxx.nodebalancer.linode.com', 'id': 'xxxxxx', 'ipv4': 'xxx.xxx.xxx.xxx', 'ipv6': 'xxxx:xxxx:x::xxxx:xxxx', 'label': 'ansible-nodebalancer', 'region': 'us-east', 'tags': [], 'transfer': {'in': None, 'out': None, 'total': None}, 'updated': '2021-03-03T17:45:37'}, 'nodes': [{'address': 'xxx.xxx.xxx.xxx:80', 'config_id': 'xxxxxx', 'id': 'xxxxxx', 'label': 'node1', 'mode': 'accept', 'nodebalancer_id': 'xxxxxx', 'status': 'Unknown', 'weight': 50}]})
  The NodeBalancer, Configs, and Nodes in JSON serialized form.





Status
------





Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)

