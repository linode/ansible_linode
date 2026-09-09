#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve VPC availability information for a Linode Region."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    region_vpc_availability_info as docs,
)
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
        display_name="Region VPC Availability",
        field_name="vpc_availability",
        field_type=FieldType.dict,
        docs_url="TODO",
        samples=docs.result_vpc_availability_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="region",
            display_name="Region",
            type=FieldType.string,
            get=lambda client, params: client.load(
                Region, params.get("region")
            ).vpc_availability._serialize(),
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
