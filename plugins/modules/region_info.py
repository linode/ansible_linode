#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Region."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.region as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.region_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Region

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Region",
        field_name="region",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-region",
        samples=docs_parent.result_region_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                Region, params.get("id")
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
