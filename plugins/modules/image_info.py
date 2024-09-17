#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode image."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Image

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Image",
        field_name="image",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-image",
        samples=docs_parent.result_image_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                Image, params.get("id")
            )._raw_json,
        ),
        InfoModuleAttr(
            name="label",
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.images,
                Image.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
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
