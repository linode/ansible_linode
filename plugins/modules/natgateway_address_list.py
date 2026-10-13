#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode NAT Gateway Addresses."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    natgateway_address_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="NAT Gateway Addresses",
    result_field_name="addresses",
    endpoint_template="/networking/natgateways/{id}/addresses",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateways",
    result_samples=docs.result_natgateway_addresses_samples,
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
