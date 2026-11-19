#!/usr/bin/python
# -*- coding: utf-8 -*-

"""List account users exempt from MFA enforcement."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    tfa_optional_user_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    tfa_optional_users as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="MFA-exempt users",
    result_field_name="tfa_optional_users",
    endpoint_template="/account/tfa-optional-users",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-tfa-optional-users",
    examples=docs.specdoc_examples,
    result_samples=docs_parent.result_tfa_optional_users_samples,
    description=[
        "List users exempt from multi-factor authentication (MFA) enforcement, "
        "regardless of the current account-wide enforcement policy."
    ],
    disable_filters=True,
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
