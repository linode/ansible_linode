#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the functionality for the Image Share Group Member info module."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    image_share_group_member_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import ImageShareGroup

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="image_share_group_member",
        field_type=FieldType.dict,
        display_name="Image Share Group Member",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroup-member-token",
        samples=docs.result_image_share_group_member_samples,
    ),
    params=[
        InfoModuleParam(
            display_name="Image Share Group",
            name="sharegroup_id",
            type=FieldType.integer,
        )
    ],
    attributes=[
        InfoModuleAttr(
            display_name="Token UUID",
            name="token_uuid",
            type=FieldType.string,
            get=lambda client, params: next(
                (
                    m.__dict__
                    for m in client.load(
                        ImageShareGroup,
                        params.get("sharegroup_id"),
                    ).get_members()
                    if m.token_uuid == params.get("token_uuid")
                ),
                None,
            ),
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: next(
                (
                    m.__dict__
                    for m in client.load(
                        ImageShareGroup,
                        params.get("sharegroup_id"),
                    ).get_members()
                    if m.label == params.get("label")
                ),
                None,
            ),
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
