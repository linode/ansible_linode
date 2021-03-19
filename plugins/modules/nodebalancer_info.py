#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode NodeBalancers."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    create_filter_and
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

# pylint: disable=unused-import
from linode_api4 import NodeBalancer, NodeBalancerConfig, NodeBalancerNode, PaginatedList, and_

DOCUMENTATION = '''
---
module: nodebalancer_info
description: Get info about a NodeBalancer.
requirements:
  - python >= 2.7
  - linode_api4 >= 3.0
author:
  - Luke Murphy (@decentral1se)
  - Charles Kenney (@charliekenney23)
  - Phillip Campbell (@phillc)
  - Lena Garber (@lbgarber)
options:
  label:
    description:
      - The label of this NodeBalancer
    type: string
    
  id:
    description:
      - The unique id of this NodeBalancer
    type: int
'''

EXAMPLES = '''
- name: Get a NodeBalancer by its id
  linode.cloud.nodebalancer_info:
    id: 12345
    
- name: Get a NodeBalancer by its label
  linode.cloud.nodebalancer_info:
    label: cool_nodebalancer
'''

RETURN = '''
nodebalancer:
  description: The NodeBalancer, Configs, and Nodes in JSON serialized form.
  returned: Always.
  type: dict
  sample: {
   "changed":false,
   "configs":[
      {
         "algorithm":"roundrobin",
         "check":"none",
         "check_attempts":3,
         "check_body":"",
         "check_interval":0,
         "check_passive":true,
         "check_path":"",
         "check_timeout":30,
         "cipher_suite":"recommended",
         "id":xxxxx,
         "nodebalancer_id":xxxxxx,
         "nodes_status":{
            "down":1,
            "up":0
         },
         "port":80,
         "protocol":"http",
         "proxy_protocol":"none",
         "ssl_cert":null,
         "ssl_commonname":"",
         "ssl_fingerprint":"",
         "ssl_key":null,
         "stickiness":"none"
      }
   ],
   "node_balancer":{
      "client_conn_throttle":0,
      "created":"2021-03-03T17:45:37",
      "hostname":"xxx.nodebalancer.linode.com",
      "id": xxxxxx,
      "ipv4":"xxx.xxx.xxx.xxx",
      "ipv6":"xxxx:xxxx:x::xxxx:xxxx",
      "label":"ansible-nodebalancer",
      "region":"us-east",
      "tags":[
         
      ],
      "transfer":{
         "in":null,
         "out":null,
         "total":null
      },
      "updated":"2021-03-03T17:45:37"
   },
   "nodes":[
      {
         "address":"xxx.xxx.xxx.xxx:80",
         "config_id": xxxxxx,
         "id": xxxxxx,
         "label":"node1",
         "mode":"accept",
         "nodebalancer_id": xxxxxx,
         "status":"Unknown",
         "weight":50
      }
   ]
}
'''

linode_nodebalancer_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False),

    id=dict(type='int', required=False),
    label=dict(type='str', required=False)
)

linode_nodebalancer_valid_filters = [
    'id', 'label'
]

class LinodeNodeBalancerInfo(LinodeModuleBase):
    """Retrieves info about a Linode NodeBalancer"""

    def __init__(self):
        self.module_arg_spec = linode_nodebalancer_info_spec
        self.required_one_of = []
        self.results = dict(
            node_balancer=None,
            configs=[],
            nodes=[]
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def get_nodebalancer_by_property(self, **kwargs):
        """Gets the NodeBalancer with the given property in kwargs"""

        filter_items = {k: v for k, v in kwargs.items()
                        if k in linode_nodebalancer_valid_filters and v is not None}

        filter_statement = create_filter_and(NodeBalancer, filter_items)

        try:
            # Special case because ID is not filterable
            if 'id' in filter_items.keys():
                result = NodeBalancer(self.client, kwargs.get('id'))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.nodebalancers(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get nodebalancer {0}'.format(exception))

    def get_node_by_label(self, config, label):
        """Gets the node within the given config by its label"""
        try:
            return config.nodes(NodeBalancerNode.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get nodebalancer node {0}, {1}'.format(label, exception))

    def exec_module(self, **kwargs):
        """Entrypoint for NodeBalancer Info module"""

        node_balancer = self.get_nodebalancer_by_property(**kwargs)

        if node_balancer is None:
            self.fail('failed to get nodebalancer')

        self.results['node_balancer'] = node_balancer._raw_json

        for config in node_balancer.configs:
            self.results['configs'].append(config._raw_json)

            for node in config.nodes:
                node._api_get()

                self.results['nodes'].append(node._raw_json)

        return self.results


def main():
    """Constructs and calls the Linode NodeBalancer Info module"""
    LinodeNodeBalancerInfo()


if __name__ == '__main__':
    main()
