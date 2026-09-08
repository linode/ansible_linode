#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Implementation for linode.cloud.vpc_default_ranges_info module."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    vpc_default_ranges as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="VPC Default Ranges",
        field_name="vpc_default_ranges",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpcs-default-ranges",
        samples=docs.result_samples,
        get=lambda client, params: client.vpcs.default_ranges()._serialize(),
    ),
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
