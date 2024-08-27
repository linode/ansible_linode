#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Users."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Users",
    result_field_name="users",
    endpoint_template="/account/users",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-users",
    examples=docs.specdoc_examples,
    result_samples=docs.result_users_samples,
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
