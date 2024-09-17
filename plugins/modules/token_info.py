#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Token."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import PersonalAccessToken

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="token",
        field_type=FieldType.dict,
        display_name="Personal Access Token",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-personal-access-tokens",
        samples=docs_parent.result_token_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                PersonalAccessToken,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.profile.tokens,
                PersonalAccessToken.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
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
