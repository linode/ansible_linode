#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode NodeBalancers."""

from __future__ import absolute_import, division, print_function

from typing import Optional, cast, Any, List, Set, Tuple

import linode_api4

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    paginated_list_to_json, dict_select_matching, filter_null_values

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase


from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

# pylint: disable=unused-import
from linode_api4 import NodeBalancer, NodeBalancerConfig, NodeBalancerNode, PaginatedList

linode_nodes_spec = dict(
    label=dict(
        type='str', required=True,
        description='The label for this node.'),

    address=dict(
        type='str', required=True,
        description=[
            'The private IP Address where this backend can be reached.',
            'This must be a private IP address.'
        ]),

    weight=dict(
        type='int', required=False,
        description='Nodes with a higher weight will receive more traffic.',
    ),

    mode=dict(
        type='str', required=False,
        description='The mode this NodeBalancer should use when sending traffic to this backend.',
        choices=['accept', 'reject', 'drain', 'backup']),

)

linode_configs_spec = dict(
    algorithm=dict(
        type='str', required=False,
        description='What algorithm this NodeBalancer should use for routing traffic to backends.',
        choices=['roundrobin', 'leastconn', 'source']),

    check=dict(
        type='str', required=False,
        description='The type of check to perform against backends to ensure they are '
                    'serving requests.',
        choices=['none', 'connection', 'http', 'http_body']),

    check_attempts=dict(
        type='int', required=False,
        description='How many times to attempt a check before considering a backend to be down.'),

    check_body=dict(
        type='str', required=False, default='',
        description=[
            'This value must be present in the response body of the check in order for it to pass.',
            'If this value is not present in the response body of a check request, the backend is '
            'considered to be down.'
        ]),

    check_interval=dict(
        type='int', required=False,
        description='How often, in seconds, to check that backends are up and serving requests.'),

    check_passive=dict(
        type='bool', required=False,
        description='If true, any response from this backend with a 5xx status code will be enough '
                    'for it to be considered unhealthy and taken out of rotation.'),

    check_path=dict(
        type='str', required=False,
        description='The URL path to check on each backend. If the backend does '
                    'not respond to this request it is considered to be down.'),

    check_timeout=dict(
        type='int', required=False,
        description='How long, in seconds, to wait for a check attempt before considering it '
                    'failed.'),

    cipher_suite=dict(
        type='str', required=False, default='recommended',
        description='What ciphers to use for SSL connections served by this NodeBalancer.',
        choices=['recommended', 'legacy']),

    port=dict(
        type='int', required=False,
        description='The port this Config is for.'),

    protocol=dict(
        type='str', required=False,
        description='The protocol this port is configured to serve.',
        choices=['http', 'https', 'tcp']),

    proxy_protocol=dict(
        type='str', required=False,
        description='ProxyProtocol is a TCP extension that sends initial TCP connection '
                    'information such as source/destination IPs and ports to backend devices.',
        choices=['none', 'v1', 'v2']),

    ssl_cert=dict(
        type='str', required=False,
        description='The PEM-formatted public SSL certificate (or the combined '
                    'PEM-formatted SSL certificate and Certificate Authority chain) '
                    'that should be served on this NodeBalancerConfig’s port.'),

    ssl_key=dict(
        type='str', required=False,
        description='The PEM-formatted private key for the SSL certificate '
                    'set in the ssl_cert field.'),

    stickiness=dict(
        type='str', required=False,
        description='Controls how session stickiness is handled on this port.',
        choices=['none', 'table', 'http_cookie']),

    nodes=dict(
        type='list', required=False, elements='dict', options=linode_nodes_spec,
        description='A list of nodes to apply to this config. '
                    'These can alternatively be configured through the nodebalancer_node module.')
)

linode_nodebalancer_spec = dict(
    label=dict(
        type='str',
        description='The unique label to give this NodeBalancer.',
        required=True,
    ),

    client_conn_throttle=dict(
        type='int',
        description=[
            'Throttle connections per second.',
            'Set to 0 (zero) to disable throttling.'
        ]),

    region=dict(
        type='str',
        description='The ID of the Region to create this NodeBalancer in.',
    ),

    configs=dict(
        type='list', elements='dict', options=linode_configs_spec,
        description='A list of configs to apply to the NodeBalancer.')
)

specdoc_examples = ['''
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
            address: 0.0.0.0:80''', '''
- name: Delete the NodeBalancer
  linode.cloud.nodebalancer:
    label: my-loadbalancer
    region: us-east
    state: absent''']

result_node_balancer_samples = ['''{
  "client_conn_throttle": 0,
  "created": "2018-01-01T00:01:01",
  "hostname": "192.0.2.1.ip.linodeusercontent.com",
  "id": 12345,
  "ipv4": "12.34.56.78",
  "ipv6": null,
  "label": "balancer12345",
  "region": "us-east",
  "tags": [
    "example tag",
    "another example"
  ],
  "transfer": {
    "in": 28.91200828552246,
    "out": 3.5487728118896484,
    "total": 32.46078109741211
  },
  "updated": "2018-03-01T00:01:01"
}''']

result_configs_samples = ['''[
  {
    "algorithm": "roundrobin",
    "check": "http_body",
    "check_attempts": 3,
    "check_body": "it works",
    "check_interval": 90,
    "check_passive": true,
    "check_path": "/test",
    "check_timeout": 10,
    "cipher_suite": "recommended",
    "id": 4567,
    "nodebalancer_id": 12345,
    "nodes_status": {
      "down": 0,
      "up": 4
    },
    "port": 80,
    "protocol": "http",
    "proxy_protocol": "none",
    "ssl_cert": null,
    "ssl_commonname": null,
    "ssl_fingerprint": null,
    "ssl_key": null,
    "stickiness": "http_cookie"
  }
]''']

result_nodes_samples = ['''[
  {
    "address": "192.168.210.120:80",
    "config_id": 4567,
    "id": 54321,
    "label": "node54321",
    "mode": "accept",
    "nodebalancer_id": 12345,
    "status": "UP",
    "weight": 50
  }
]''']

specdoc_meta = dict(
    description=[
        'Manage a Linode NodeBalancer.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_nodebalancer_spec,
    examples=specdoc_examples,
    return_values=dict(
        node_balancer=dict(
            description='The NodeBalancer in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/nodebalancers/#nodebalancer-view__responses',
            type='dict',
            sample=result_node_balancer_samples
        ),
        configs=dict(
            description='A list of configs applied to the NodeBalancer.',
            docs_url='https://www.linode.com/docs/api/nodebalancers/#config-view__responses',
            type='list',
            sample=result_configs_samples
        ),
        nodes=dict(
            description='A list of configs applied to the NodeBalancer.',
            docs_url='https://www.linode.com/docs/api/nodebalancers/#node-view',
            type='list',
            sample=result_nodes_samples
        )
    )
)

linode_nodebalancer_mutable: Set[str] = {
    'client_conn_throttle',
    'tags'
}


class LinodeNodeBalancer(LinodeModuleBase):
    """Configuration class for Linode NodeBalancer resource"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_nodebalancer_spec
        self.required_one_of = ['state', 'label']
        self.results = dict(
            changed=False,
            actions=[],
            node_balancer=None,
            configs=[],
            nodes=[]
        )

        self._node_balancer: Optional[NodeBalancer] = None

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def _get_nodebalancer_by_label(self, label: str) -> Optional[NodeBalancer]:
        """Gets the NodeBalancer with the given label"""

        try:
            return self.client.nodebalancers(NodeBalancer.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get nodebalancer {0}: {1}'.format(label, exception))

    def _get_node_by_label(self, config: NodeBalancerConfig, label: str) \
            -> Optional[NodeBalancerNode]:
        """Gets the node within the given config by its label"""
        try:
            return config.nodes(NodeBalancerNode.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get nodebalancer node {0}, {1}'
                             .format(label, exception))

    def _create_nodebalancer(self) -> Optional[NodeBalancer]:
        """Creates a NodeBalancer with the given kwargs"""

        params = self.module.params
        label = params.get('label')
        region = params.get('region')

        try:
            return self.client.nodebalancer_create(region, label=label)
        except Exception as exception:
            return self.fail(msg='failed to create nodebalancer: {0}'.format(exception))

    def _create_config(self, node_balancer: NodeBalancer, config_params: dict) \
            -> Optional[NodeBalancerConfig]:
        """Creates a config with the given kwargs within the given NodeBalancer"""

        try:
            return node_balancer.config_create(None, **config_params)
        except Exception as exception:
            return self.fail(msg='failed to create nodebalancer config: {0}'.format(exception))

    def _create_node(self, config: NodeBalancerConfig, node_params: dict) \
            -> Optional[NodeBalancerNode]:
        """Creates a node with the given kwargs within the given config"""

        label = node_params.pop('label')

        try:
            return config.node_create(label, **node_params)
        except Exception as exception:
            return self.fail(msg='failed to create nodebalancer node: {0}'.format(exception))

    def _create_config_register(self, node_balancer: NodeBalancer, config_params: dict) \
            -> NodeBalancerConfig:
        """Registers a create action for the given config"""

        config = self._create_config(node_balancer, config_params)
        self.register_action('Created config: {0}'.format(config.id))

        return config

    def _delete_config_register(self, config: NodeBalancerConfig) -> None:
        """Registers a delete action for the given config"""

        self.register_action('Deleted config: {0}'.format(config.id))
        config.delete()

    def _create_node_register(self, config: NodeBalancerConfig, node_params: dict) \
            -> NodeBalancerNode:
        """Registers a create action for the given node"""

        node = self._create_node(config, node_params)
        self.register_action('Created Node: {0}'.format(node.id))

        return node

    def _delete_node_register(self, node: NodeBalancerNode) -> None:
        """Registers a delete action for the given node"""

        self.register_action('Deleted Node: {0}'.format(node.id))
        node.delete()

    def _handle_config_nodes(self, config: NodeBalancerConfig, new_nodes: List[dict]) -> None:
        """Updates the NodeBalancer nodes defined in new_nodes within the given config"""

        node_map = {}
        nodes = config.nodes

        for node in nodes:
            node._api_get()
            node_map[node.label] = node

        for node in new_nodes:
            node_label = node.get('label')

            if node_label in node_map:
                node_match, remote_node_match = dict_select_matching(
                    filter_null_values(node), node_map[node_label]._raw_json)

                if node_match == remote_node_match:
                    del node_map[node_label]
                    continue

                self._delete_node_register(node_map[node_label])

            self._create_node_register(config, node)

        for node in node_map.values():
            self._delete_node_register(node)

    @staticmethod
    def _check_config_exists(target: Set[NodeBalancerConfig], config: dict) \
            -> Tuple[bool, Optional[NodeBalancerConfig]]:
        """Returns whether a config exists in the target set"""

        for remote_config in target:
            config_match, remote_config_match = \
                dict_select_matching(filter_null_values(config), remote_config._raw_json)

            if config_match == remote_config_match:
                return True, remote_config

        return False, None

    def _handle_configs(self) -> None:
        """Updates the configs defined in new_configs under this NodeBalancer"""

        new_configs = self.module.params.get('configs') or []
        remote_configs = set(self._node_balancer.configs)

        for config in new_configs:
            config_exists, remote_config = self._check_config_exists(remote_configs, config)

            if config_exists:
                if config.get('nodes') is not None:
                    self._handle_config_nodes(remote_config, config.get('nodes'))
                remote_configs.remove(remote_config)
                continue

            new_config = self._create_config_register(self._node_balancer, config)
            if config.get('nodes') is not None:
                self._handle_config_nodes(new_config, config.get('nodes'))

        # Remove remaining configs
        for config in remote_configs:
            self._delete_config_register(config)

        cast(list, self.results['configs']) \
            .extend(paginated_list_to_json(self._node_balancer.configs))

    def _update_nodebalancer(self) -> None:
        """Update instance handles all update functionality for the current nodebalancer"""
        should_update = False

        params = filter_null_values(self.module.params)

        # "configs" is defined in NodeBalancer, but is a property method
        if 'configs' in params.keys():
            params.pop('configs')

        for key, new_value in params.items():
            if not hasattr(self._node_balancer, key):
                continue

            old_value = getattr(self._node_balancer, key)

            if isinstance(old_value, linode_api4.objects.linode.Region):
                old_value = old_value.id

            if new_value != old_value:
                if key in linode_nodebalancer_mutable:
                    setattr(self._node_balancer, key, new_value)
                    self.register_action('Updated nodebalancer {0}: "{1}" -> "{2}"'.
                                         format(key, old_value, new_value))

                    should_update = True
                    continue

                self.fail(
                    'failed to update nodebalancer {0}: {1} is a non-updatable field'
                        .format(self._node_balancer.label, key))

        if should_update:
            self._node_balancer.save()

    def _handle_nodebalancer(self) -> None:
        """Updates the NodeBalancer defined in kwargs"""

        nb_label: str = self.module.params.get('label')

        self._node_balancer = self._get_nodebalancer_by_label(nb_label)

        # Create NodeBalancer if doesn't exist
        if self._node_balancer is None:
            self._node_balancer = self._create_nodebalancer()
            self.register_action('Created NodeBalancer {}'.format(nb_label))

        if self._node_balancer is None:
            return self.fail('failed to create nodebalancer')

        self._update_nodebalancer()
        self._node_balancer._api_get()

        self.results['node_balancer'] = self._node_balancer._raw_json

    def _handle_nodebalancer_absent(self) -> None:
        """Updates the NodeBalancer for the absent state"""

        label = self.module.params.get('label')

        self._node_balancer = self._get_nodebalancer_by_label(label)

        if self._node_balancer is not None:
            self.results['node_balancer'] = self._node_balancer._raw_json
            self._node_balancer.delete()
            self.register_action('Deleted NodeBalancer {}'.format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for NodeBalancer module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_nodebalancer_absent()
            return self.results

        self._handle_nodebalancer()
        self._handle_configs()

        # Append all nodes to the result
        for config in self._node_balancer.configs:
            for node in config.nodes:
                node._api_get()
                cast(list, self.results['nodes']).append(node._raw_json)

        return self.results


def main() -> None:
    """Constructs and calls the Linode NodeBalancer module"""
    LinodeNodeBalancer()


if __name__ == '__main__':
    main()
