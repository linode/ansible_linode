#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Placement Group info."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    placement_group_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import PlacementGroup

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Placement Group",
        field_name="placement_group",
        field_type=FieldType.dict,
        docs_url="TBD",
        samples=docs.result_placement_group_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                PlacementGroup, params.get("id")
            )._raw_json,
        ),
    ],
    requires_beta=True,
)

SPECDOC_META = module.spec

if __name__ == "__main__":
    module.run()
