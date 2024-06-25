#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Child Account."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    child_account_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import ChildAccount

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="child_account",
        field_type=FieldType.dict,
        display_name="Child Account",
        docs_url="",
        samples=docs.result_child_account_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="EUUID",
            name="euuid",
            type=FieldType.string,
            get=lambda client, params: client.load(
                ChildAccount,
                params.get("euuid"),
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
    description=[
       "Get info about a Linode Child Account.", "NOTE: Parent/Child related features may not be generally available."
    ],
)

SPECDOC_META = module.spec

if __name__ == "__main__":
    module.run()
