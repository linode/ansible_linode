#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Child Account."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.child_account_info as docs
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
            type=FieldType.integer,
            get=lambda client, params: client.load(
                ChildAccount,
                params.get("euuid"),
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
)

SPECDOC_META = module.spec

if __name__ == "__main__":
    module.run()
