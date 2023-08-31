#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing Linode VPCs."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModuleBase,
)


class ListModule(ListModuleBase):
    """
    Allows users to list VPCs that meet a set of filters.
    """

    display_name = "VPC"
    result_field = "vpcs"
    endpoint = "/vpcs"
    docs_url = "TODO"
    examples = docs.specdoc_examples
    response_samples = docs.result_vpc_samples


SPECDOC_META = ListModule.spec

if __name__ == "__main__":
    ListModule()
