#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for listing Linode Account Children."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    child_account_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

RESULT_DISPLAY_NAME = "Child Account"

module = ListModule(
    result_display_name=RESULT_DISPLAY_NAME,
    result_field_name="child_accounts",
    endpoint_template="/account/child-accounts",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-child-accounts",
    examples=docs.specdoc_examples,
    result_samples=docs.result_child_accounts_samples,
    description=[
        f"List and filter on {RESULT_DISPLAY_NAME}.",
        "NOTE: Parent/Child related features may not be generally available.",
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
