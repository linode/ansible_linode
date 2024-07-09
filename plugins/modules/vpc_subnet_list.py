#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the functionality for listing subnets under a VPC."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="VPC Subnets",
    result_field_name="subnets",
    endpoint_template="/vpcs/{vpc_id}/subnets",
    result_docs_url="",
    result_samples=docs.result_vpc_samples,
    examples=docs.specdoc_examples,
    params=[
        ListModuleParam(
            display_name="VPC", name="vpc_id", type=FieldType.integer
        )
    ],
)


SPECDOC_META = module.spec

DOCUMENTATION = """
"""
EXAMPLES = """
"""
RETURN = """
"""

if __name__ == "__main__":
    module.run()
