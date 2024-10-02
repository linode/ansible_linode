#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Network Transfer Prices."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    network_transfer_prices_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Network Transfer Prices",
    result_field_name="network_transfer_prices",
    endpoint_template="/network-transfer/prices",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-network-transfer-prices",
    examples=docs.specdoc_examples,
    result_samples=docs.result_network_transfer_prices_samples,
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
