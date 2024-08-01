#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode user."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import User

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="user",
        field_type=FieldType.dict,
        display_name="User",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-user",
        samples=docs.result_user_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="grants",
            field_type=FieldType.dict,
            display_name="Grants",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-user-grants",
            samples=docs.result_grants_samples,
            get=lambda client, user, params: client.get(
                # We can't use the UserGrants type here because
                # it does not serialize directly to JSON or store
                # the API response JSON.
                f"/account/users/{user['username']}/grants"
            ),
        )
    ],
    attributes=[
        InfoModuleAttr(
            name="username",
            display_name="Username",
            type=FieldType.string,
            get=lambda client, params: client.load(
                User, params.get("username")
            )._raw_json,
        )
    ],
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
