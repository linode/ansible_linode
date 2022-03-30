.. _nodebalancer_node_module:


nodebalancer_node
=================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode NodeBalancer Nodes.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **config_id (Required, type=int):**
    \• The ID of the NodeBalancer Config that contains this node.


  **label (Required, type=str):**
    \• The label for this node. This is used to identify nodes within a config.


  **nodebalancer_id (Required, type=int):**
    \• The ID of the NodeBalancer that contains this node.


  **state (Required, type=str):**
    \• Whether the NodeBalancer node should be present or absent.

    \• Options: `present`, `absent`



  **address (type=str):**
    \• The private IP Address where this backend can be reached. This must be a private IP address.


  **mode (type=str):**
    \• The mode this NodeBalancer should use when sending traffic to this backend.

    \• Options: `accept`, `reject`, `drain`, `backup`


  **weight (type=int):**
    \• Nodes with a higher weight will receive more traffic.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a NodeBalancer
      linode.cloud.nodebalancer:
        label: my-nodebalancer
        region: us-east
        state: present
        configs:
          - port: 80
            protocol: http
            algorithm: roundrobin
      register: nodebalancer_result
            
    - name: Create an Instance
      linode.cloud.instance:
        label: my-instance
        region: us-east
        private_ip: true
        type: g6-standard-1
        state: present
      register: instance_result
        
    - name: Attach the Instance to the NodeBalancer
      linode.cloud.nodebalancer_node:
        nodebalancer_id = nodebalancer_result.node_balancer.id
        config_id = nodebalancer_result.configs[0].id
        
        label: my-node
        
        # Use the private ip address of the instance
        address: '{{ instance_result.instance.ipv4[1] }}:80'




Return Values
-------------

**node (returned=always, type=dict):**

The NodeBalancer Node in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/nodebalancers/#node-view__responses>`_

Sample Response:

.. code-block:: JSON

    {
     "address": "123.123.123.123:80",
     "config_id": 12345,
     "id": 12345,
     "label": "mynode",
     "mode": "accept",
     "nodebalancer_id": 12345,
     "status": "Unknown",
     "weight": 10
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

