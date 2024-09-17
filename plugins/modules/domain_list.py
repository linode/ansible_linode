#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file contains the implementation of the domain_list module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Domains",
    result_field_name="domains",
    endpoint_template="/domains",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-domains",
    examples=docs.specdoc_examples,
    result_samples=docs.result_domains_samples,
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
