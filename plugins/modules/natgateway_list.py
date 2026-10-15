#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode NAT Gateways."""

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.natgateway_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="NAT Gateways",
    result_field_name="natgateways",
    endpoint_template="/networking/natgateways",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateways",
    result_samples=docs.result_natgateways_samples,
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
