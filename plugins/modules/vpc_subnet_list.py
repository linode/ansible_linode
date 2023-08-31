#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the functionality for listing subnets under a VPC."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModuleBase,
    ListModuleParent,
)
from ansible_specdoc.objects import FieldType


class ListModule(ListModuleBase):
    """
    Allows users to list subnets under a given VPC.
    """

    display_name = "VPC Subnet"
    result_field = "subnets"
    endpoint = "/vpcs/{vpc_id}/subnets"
    docs_url = "TODO"
    parents = [ListModuleParent("vpc_id", "VPC", FieldType.integer)]
    examples = docs.specdoc_examples
    response_samples = docs.result_vpc_samples


SPECDOC_META = ListModule.spec

if __name__ == "__main__":
    ListModule()
