#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing Linode Node Balancers."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.nodebalancer_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Node Balancers",
    result_field_name="nodebalancers",
    endpoint_template="/nodebalancers",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancers",
    examples=docs.specdoc_examples,
    result_samples=docs.result_nodebalancers_samples,
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
