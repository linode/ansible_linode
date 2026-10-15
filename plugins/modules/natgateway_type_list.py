#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list NAT Gateway Types."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    natgateway_type_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="NAT Gateway Types",
    result_field_name="natgateway_types",
    endpoint_template="/networking/natgateways/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateway-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_natgateway_type_samples,
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
