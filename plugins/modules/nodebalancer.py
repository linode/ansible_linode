#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode NodeBalancers."""

from __future__ import absolute_import, division, print_function

import copy
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    paginated_list_to_json, dict_select_matching
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

# pylint: disable=unused-import
from linode_api4 import NodeBalancer, NodeBalancerConfig, NodeBalancerNode, PaginatedList

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
---
module: nodebalancer
description: Manage Linode NodeBalancers.
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
      - The unique label to give this NodeBalancer
    required: true
    type: string
  region:
    description:
      - The location to deploy the instance in.
      - See U(https://api.linode.com/v4/regions)
    required: true
    type: str

  configs:
    description:
      - A list of configs to be added to the NodeBalancer.
    required: false
    type: list
    elements: dict
    suboptions:
      algorithm:
        description:
          - What algorithm this NodeBalancer should use for routing traffic to backends.
        choices:
          - roundrobin
          - leastconn
          - source
        type: str

      check:
        description:
          - The type of check to perform against backends to ensure they are serving requests.
          - This is used to determine if backends are up or down.
        choices:
          - none
          - connection
          - http
          - http_body
        type: str

      check_attempts:
        description:
          - How many times to attempt a check before considering a backend to be down.
        type: int

      check_body:
        description:
          - This value must be present in the response body of the check in order for it to pass.
          - If this value is not present in the response body of a check request, the backend is considered to be down.
        type: str

      check_interval:
        description:
          - How often, in seconds, to check that backends are up and serving requests.
        type: int

      check_passive:
        description:
          - If true, any response from this backend with a 5xx status code will be enough for it to be considered unhealthy and taken out of rotation.
        type: bool

      check_path:
        description:
          - The URL path to check on each backend. If the backend does not respond to this request it is considered to be down.
        type: str

      check_timeout:
        description:
          - How long, in seconds, to wait for a check attempt before considering it failed.
        type: int

      cipher_suite:
        description:
          - What ciphers to use for SSL connections served by this NodeBalancer.
          - C(legacy) is considered insecure and should only be used if necessary.
        choices:
          - recommended
          - legacy
        default: recommended
        type: str

      port:
        description:
          - The port for the Config to listen on.
        type: int

      protocol:
        description:
          - The protocol this port is configured to serve.
        choices:
          - http
          - https
          - tcp
        type: str

      proxy_protocol:
        description:
          - ProxyProtocol is a TCP extension that sends initial TCP connection information such as source/destination IPs and ports to backend devices.
        choices:
          - none
          - v1
          - v2
        type: str

      ssl_cert:
        description:
          - The PEM-formatted public SSL certificate (or the combined PEM-formatted SSL certificate and Certificate Authority chain) that should be served on this NodeBalancerConfig’s port.
        type: str

      ssl_key:
        description:
          - The PEM-formatted private key for the SSL certificate set in the ssl_cert field.
        type: str

      stickiness:
        description:
          - Controls how session stickiness is handled on this port.
        choices:
          - none
          - table
          - http_cookie
        type: str

      nodes:
        description:
          - A list of Nodes to be created with the parent Config.
        type: list
        elements: dict
        suboptions:
          label:
            description:
              - The label to give to this Node.
            type: str
            required: true

          address:
            description:
              - The private IP Address where this backend can be reached.
            type: str
            required: true

          mode:
            description:
              - The mode this NodeBalancer should use when sending traffic to this backend.
            choices:
              - accept
              - reject
              - drain
              - backup
            type: str

          weight:
            description:
              - Nodes with a higher weight will receive more traffic.
            type: int
'''

EXAMPLES = '''
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
'''

RETURN = '''
nodebalancer:
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

linode_nodes_spec = dict(
    label=dict(type='str', required=True),
    address=dict(type='str', required=True),
    weight=dict(type='int', required=False),
    mode=dict(type='str', required=False),
)

linode_configs_spec = dict(
    algorithm=dict(type='str', required=False),
    check=dict(type='str', required=False),
    check_attempts=dict(type='int', required=False),
    check_body=dict(type='str', required=False, default=''),
    check_interval=dict(type='int', required=False),
    check_passive=dict(type='bool', required=False),
    check_path=dict(type='str', required=False),
    check_timeout=dict(type='int', required=False),
    cipher_suite=dict(type='str', required=False, default='recommended'),
    port=dict(type='int', required=False),
    protocol=dict(type='str', required=False),
    proxy_protocol=dict(type='str', required=False),
    ssl_cert=dict(type='str', required=False),
    ssl_key=dict(type='str', required=False),
    stickiness=dict(type='str', required=False),
    nodes=dict(type='list', required=False, elements='dict', options=linode_nodes_spec)
)

linode_nodebalancer_spec = dict(
    region=dict(type='str', required=False),
    configs=dict(type='list', required=False, elements='dict', options=linode_configs_spec)
)


class LinodeNodeBalancer(LinodeModuleBase):
    """Configuration class for Linode NodeBalancer resource"""

    def __init__(self):
        self.module_arg_spec = linode_nodebalancer_spec
        self.required_one_of = ['state', 'label']
        self.results = dict(
            changed=False,
            actions=[],
            node_balancer=None,
            configs=[],
            nodes=[]
        )

        self._node_balancer = None

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def get_nodebalancer_by_label(self, label):
        """Gets the NodeBalancer with the given label"""

        try:
            return self.client.nodebalancers(NodeBalancer.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get nodebalancer {0}: {1}'.format(label, exception))

    def get_node_by_label(self, config, label):
        """Gets the node within the given config by its label"""
        try:
            return config.nodes(NodeBalancerNode.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get nodebalancer node {0}, {1}'.format(label, exception))

    def create_nodebalancer(self, **kwargs):
        """Creates a NodeBalancer with the given kwargs"""

        region = kwargs.pop('region')

        try:
            return self.client.nodebalancer_create(region, **kwargs)
        except Exception as exception:
            self.fail(msg='failed to create nodebalancer: {0}'.format(exception))

    def create_config(self, node_balancer, **kwargs):
        """Creates a config with the given kwargs within the given NodeBalancer"""

        try:
            return node_balancer.config_create(None, **kwargs)
        except Exception as exception:
            self.fail(msg='failed to create nodebalancer config: {0}'.format(exception))

    def create_node(self, config, **kwargs):
        """Creates a node with the given kwargs within the given config"""

        label = kwargs.pop('label')

        try:
            return config.node_create(label, **kwargs)
        except Exception as exception:
            self.fail(msg='failed to create nodebalancer node: {0}'.format(exception))

    def __handle_config_nodes(self, config, new_nodes):
        """Updates the NodeBalancer nodes defined in new_nodes within the given config"""

        new_nodes = new_nodes or []

        nodes = config.nodes

        # We have to do this to fix lazy loading
        for node in nodes:
            node._api_get()

        # Remove unspecified nodes
        for remote_node in nodes:
            should_delete = True

            for node in new_nodes:
                node_match, remote_node_match = dict_select_matching(node, remote_node._raw_json)

                if node_match == remote_node_match:
                    should_delete = False
                    break

            if should_delete:
                self.register_action('Deleted Node {}'.format(remote_node.label))
                remote_node.delete()

        # Create specified nodes that do not exist
        for node in new_nodes:
            exists = False
            current_node = None

            for remote_node in nodes:
                node_match, remote_node_match = dict_select_matching(node, remote_node._raw_json)

                if node_match == remote_node_match:
                    exists = True
                    current_node = remote_node

            if not exists:
                current_node = self.create_node(config, **node)
                self.register_action('Created Node {}'.format(current_node.label))

            self.results['nodes'].append(current_node._raw_json)

    def __handle_configs(self, **kwargs):
        """Updates the configs defined in kwargs under the instance's NodeBalancer"""

        configs = kwargs.get('configs')
        configs = configs or []

        remote_configs = copy.deepcopy(self._node_balancer.configs)

        # Remove unspecified configs
        for remote_config in remote_configs:
            should_delete = True

            for config in configs:
                config_match, remote_config_match = dict_select_matching(
                    config, remote_config._raw_json)

                if config_match == remote_config_match:
                    should_delete = False
                    break

            if should_delete:
                self.register_action('Deleted Config {}'.format(remote_config.id))
                remote_config.delete()

        # Create specified configs that do not exist
        for config in configs:
            config_current = None
            exists = False

            for remote_config in remote_configs:
                config_match, remote_config_match = dict_select_matching(
                    config, remote_config._raw_json)

                if config_match == remote_config_match:
                    exists = True
                    config_current = remote_config

            if not exists:
                config_current = self.create_config(self._node_balancer, **config)
                self.register_action('Created Config {}'.format(config_current.id))

            self.__handle_config_nodes(config_current, config.get('nodes'))

        self.results['configs'].extend(paginated_list_to_json(self._node_balancer.configs))

    def __handle_nodebalancer(self, **kwargs):
        """Updates the NodeBalancer defined in kwargs"""

        nb_label = kwargs.get('label')
        self._node_balancer = self.get_nodebalancer_by_label(nb_label)

        # Create NodeBalancer if doesn't exist
        if self._node_balancer is None:
            self._node_balancer = self.create_nodebalancer(
                label=nb_label,
                region=kwargs.get('region')
            )

            self.register_action('Created NodeBalancer {}'.format(nb_label))

        self.results['node_balancer'] = self._node_balancer._raw_json

    def __handle_nodebalancer_absent(self, **kwargs):
        """Updates the NodeBalancer for the absent state"""

        nb_label = kwargs.get('label')
        self._node_balancer = self.get_nodebalancer_by_label(nb_label)

        if self._node_balancer is not None:
            self.results['node_balancer'] = self._node_balancer._raw_json
            self._node_balancer.delete()
            self.register_action('Deleted NodeBalancer {}'.format(nb_label))

    def exec_module(self, **kwargs):
        """Entrypoint for NodeBalancer module"""
        state = kwargs.get('state')

        if state == 'absent':
            self.__handle_nodebalancer_absent(**kwargs)
            return self.results

        self.__handle_nodebalancer(**kwargs)
        self.__handle_configs(**kwargs)

        return self.results


def main():
    """Constructs and calls the Linode NodeBalancer module"""
    LinodeNodeBalancer()


if __name__ == '__main__':
    main()
