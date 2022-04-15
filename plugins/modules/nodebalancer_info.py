#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode NodeBalancers."""

from __future__ import absolute_import, division, print_function

from typing import List, Optional, Any

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    create_filter_and
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

# pylint: disable=unused-import
from linode_api4 import NodeBalancer, NodeBalancerConfig, NodeBalancerNode, PaginatedList, and_

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)
description:
- Get info about a Linode NodeBalancer.
module: nodebalancer_info
options:
  id:
    description: The ID of this NodeBalancer.
    required: false
    type: int
  label:
    description: The label of this NodeBalancer.
    required: false
    type: str
requirements:
- python >= 3
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
node_balancer:
  description: The NodeBalancer in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/nodebalancers/#nodebalancer-view__responses"
  returned: always
  type: dict
  sample: {
      "client_conn_throttle": 0,
      "created": "",
      "hostname": "xxxx.newark.nodebalancer.linode.com",
      "id": xxxxxx,
      "ipv4": "xxx.xxx.xxx.xxx",
      "ipv6": "xxxx:xxxx::xxxx:xxxx:xxxx:xxxx",
      "label": "my-loadbalancer",
      "region": "us-east",
      "tags": [

      ],
      "transfer": {
        "in": 0,
        "out": 0,
        "total": 0
      },
      "updated": ""
    }
    
configs:
  description: A list of configs applied to the NodeBalancer.
  linode_api_docs: "https://www.linode.com/docs/api/nodebalancers/#config-view__responses"
  returned: always
  type: list
  sample: [
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
        "id": xxxxxx,
        "nodebalancer_id": xxxxxx,
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
    
nodes:
  description: A list of all nodes associated with the NodeBalancer.
  linode_api_docs: "https://www.linode.com/docs/api/nodebalancers/#node-view__responses"
  returned: always
  type: list
  sample: [
      {
        "address": "xxx.xxx.xxx.xx:80",
        "config_id": xxxxxx,
        "id": xxxxxx,
        "label": "node1",
        "mode": "accept",
        "nodebalancer_id": xxxxxx,
        "status": "Unknown",
        "weight": 1
      }
    ]
'''

linode_nodebalancer_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False, doc_hide=True),

    id=dict(
        type='int', required=False,
        description='The ID of this NodeBalancer.'),

    label=dict(
        type='str', required=False,
        description='The label of this NodeBalancer.')
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode NodeBalancer.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_nodebalancer_info_spec
)

linode_nodebalancer_valid_filters = [
    'id', 'label'
]


class LinodeNodeBalancerInfo(LinodeModuleBase):
    """Module for getting info about a Linode NodeBalancer"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_nodebalancer_info_spec
        self.required_one_of: List[str] = []
        self.results: dict = dict(
            node_balancer=None,
            configs=[],
            nodes=[]
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def _get_matching_nodebalancer(self) -> Optional[NodeBalancer]:
        filter_items = {k: v for k, v in self.module.params.items()
                        if k in linode_nodebalancer_valid_filters and v is not None}

        filter_statement = create_filter_and(NodeBalancer, filter_items)

        try:
            # Special case because ID is not filterable
            if 'id' in filter_items.keys():
                result = NodeBalancer(self.client, self.module.params.get('id'))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.nodebalancers(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get nodebalancer {0}'.format(exception))

    def _get_node_by_label(self, config: NodeBalancerConfig, label: str) \
            -> Optional[NodeBalancerNode]:
        try:
            return config.nodes(NodeBalancerNode.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get nodebalancer node {0}, {1}'
                             .format(label, exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for NodeBalancer Info module"""

        node_balancer = self._get_matching_nodebalancer()

        if node_balancer is None:
            return self.fail('failed to get nodebalancer')

        self.results['node_balancer'] = node_balancer._raw_json

        for config in node_balancer.configs:
            self.results['configs'].append(config._raw_json)

            for node in config.nodes:
                node._api_get()

                self.results['nodes'].append(node._raw_json)

        return self.results


def main() -> None:
    """Constructs and calls the Linode NodeBalancer Info module"""
    LinodeNodeBalancerInfo()


if __name__ == '__main__':
    main()
