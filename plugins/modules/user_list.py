#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Users."""

from typing import Any

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user_list as docs
from ansible.module_utils.parsing.convert_bool import boolean
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    construct_api_filter,
)


def _construct_user_filter(params: dict[str, Any]) -> dict[str, Any]:
    """Serialize MFA enforcement filters as booleans, not strings."""
    api_filter = construct_api_filter(params)
    for group in api_filter["+and"]:
        for condition in group["+or"]:
            if "tfa_enforced" in condition:
                condition["tfa_enforced"] = boolean(condition["tfa_enforced"])
    return api_filter


module = ListModule(
    result_display_name="Users",
    result_field_name="users",
    endpoint_template="/account/users",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-users",
    examples=docs.specdoc_examples,
    result_samples=docs.result_users_samples,
    custom_api_filter_constructor=_construct_user_filter,
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
