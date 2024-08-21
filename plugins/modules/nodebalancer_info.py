#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode NodeBalancer."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    paginated_list_to_json,
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import LinodeClient, NodeBalancer


def _get_firewalls_data(
    client: LinodeClient, nodebalancer: NodeBalancer, params: Dict[str, Any]
) -> List[Any]:
    firewalls = NodeBalancer(client, nodebalancer["id"]).firewalls()
    firewalls_json = []
    for firewall in firewalls:
        firewall._api_get()
        firewalls_json.append(firewall._raw_json)
    return firewalls_json


def _get_nodes(
    client: LinodeClient, nodebalancer: NodeBalancer, params: Dict[str, Any]
) -> List[Any]:
    configs = NodeBalancer(client, nodebalancer["id"]).configs
    nodes_json = []
    for config in configs:
        for node in config.nodes:
            node._api_get()
            nodes_json.append(node._raw_json)
    return nodes_json


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="node_balancer",
        field_type=FieldType.dict,
        display_name="Node Balancer",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer",
        samples=docs_parent.result_node_balancer_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="configs",
            field_type=FieldType.list,
            display_name="configs",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-configs",
            samples=docs_parent.result_configs_samples,
            get=lambda client, nodebalancer, params: paginated_list_to_json(
                NodeBalancer(client, nodebalancer["id"]).configs
            ),
        ),
        InfoModuleResult(
            field_name="nodes",
            field_type=FieldType.list,
            display_name="nodes",
            docs_url="https://techdocs.akamai.com/linode-api/"
            + "reference/get-node-balancer-config-nodes",
            samples=docs_parent.result_nodes_samples,
            get=_get_nodes,
        ),
        InfoModuleResult(
            field_name="firewalls",
            field_type=FieldType.list,
            display_name="firewalls",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-firewalls",
            samples=docs_parent.result_firewalls_samples,
            get=lambda client, nodebalancer, params: [
                firewall.id
                for firewall in NodeBalancer(
                    client, nodebalancer["id"]
                ).firewalls()
            ],
        ),
        InfoModuleResult(
            field_name="firewalls_data",
            field_type=FieldType.list,
            display_name="firewalls_data",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-firewalls",
            samples=docs_parent.result_firewalls_data_samples,
            get=_get_firewalls_data,
        ),
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                NodeBalancer,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.nodebalancers,
                NodeBalancer.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
)


SPECDOC_META = module.spec

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

if __name__ == "__main__":
    module.run()
