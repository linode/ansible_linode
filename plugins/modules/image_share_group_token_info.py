#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the functionality for the Image Share Group Token info module."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    image_share_group_token_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import ImageShareGroupToken

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="image_share_group_token",
        field_type=FieldType.dict,
        display_name="Image Share Group Token",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroup-token",
        samples=docs.result_image_share_group_token_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="Token UUID",
            name="token_uuid",
            type=FieldType.string,
            get=lambda client, params: client.load(
                ImageShareGroupToken,
                params.get("token_uuid"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.sharegroups.tokens,
                ImageShareGroupToken.label == params.get("label"),
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
