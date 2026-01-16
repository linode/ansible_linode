#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the functionality for the Consumer Image Share Group info module.
This module allows a consumer to retrieve information about the Image Share Group a specific
Image Share Group Token gives access to."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    consumer_image_share_group_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleParam,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import ImageShareGroupToken

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="image_share_group",
        field_type=FieldType.dict,
        display_name="Image Share Group",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroup-by-token",
        samples=docs.result_consumer_image_share_group_samples,
        get=lambda client, params, _current=None: (
            client.load(ImageShareGroupToken, params["token_uuid"])
            .get_sharegroup()
            .__dict__
        ),
    ),
    params=[
        InfoModuleParam(
            display_name="Token",
            name="token_uuid",
            type=FieldType.string,
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
