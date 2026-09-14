#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for
listing Linode Node Balancer VPC configurations."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_vpc_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="Node Balancer VPC Configurations",
    result_field_name="nodebalancer_vpc_configs",
    endpoint_template="/nodebalancers/{nodebalancer_id}/vpcs",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-vpcs",
    examples=docs.specdoc_examples,
    result_samples=docs.result_nodebalancer_vpcs_samples,
    params=[
        ListModuleParam(
            display_name="NodeBalancer",
            name="nodebalancer_id",
            type=FieldType.integer,
        )
    ],
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
