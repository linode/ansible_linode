#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list a Linode NAT Gateway's Interfaces
that are actively using the specified NAT Gateway IP Address."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    natgateway_interface_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="NAT Gateway Interfaces",
    result_field_name="interfaces",
    endpoint_template="/networking/natgateways/{id}/interfaces",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateway-interfaces",
    result_samples=docs.result_natgateway_interface_samples,
    examples=docs.specdoc_examples,
    params=[
        ListModuleParam(
            display_name="NAT Gateway",
            name="id",
            type=FieldType.integer,
        ),
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
