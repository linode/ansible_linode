#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode VPC Subnet."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import VPC, LinodeClient, VPCSubnet


def _subnet_by_label(
    client: LinodeClient, params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Gets a subnet with the given params using the `label` attribute.
    """

    label = params.get("label")
    vpc = client.load(VPC, params.get("vpc_id"))
    return safe_find(
        lambda: [v for v in vpc.subnets if v.label == label],
        raise_not_found=True,
    )._raw_json


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="subnet",
        field_type=FieldType.dict,
        display_name="VPC Subnet",
        docs_url="",
        samples=docs_parent.result_subnet_samples,
    ),
    params=[
        InfoModuleParam(
            display_name="VPC", name="vpc_id", type=FieldType.integer
        )
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                VPCSubnet,
                params.get("id"),
                target_parent_id=params.get("vpc_id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=_subnet_by_label,
        ),
    ],
    examples=docs.specdoc_examples,
)

SPECDOC_META = module.spec

DOCUMENTATION = '''
'''
EXAMPLES = '''
'''
RETURN = '''
'''

if __name__ == "__main__":
    module.run()
