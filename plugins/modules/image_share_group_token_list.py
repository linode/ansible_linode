#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Image Share Group Tokens."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    image_share_group_token_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Image Share Group Tokens",
    result_field_name="image_share_group_tokens",
    endpoint_template="/images/sharegroups/tokens",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-user-tokens",
    result_samples=docs.result_image_share_group_tokens_samples,
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
