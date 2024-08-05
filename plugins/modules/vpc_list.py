#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing Linode VPCs."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="VPCs",
    result_field_name="vpcs",
    endpoint_template="/vpcs",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpcs",
    examples=docs.specdoc_examples,
    result_samples=docs.result_vpc_samples,
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
