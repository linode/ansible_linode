#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the implementation of the region_vpc_availability_list module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.region_vpc_availability_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Region VPC Availability",
    result_field_name="vpc_availabilities",
    endpoint_template="/regions/vpc-availability",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-regions-vpc-availability",
    examples=docs.specdoc_examples,
    result_samples=docs.result_vpc_availabilities_samples,
    description=[
        "List and filter on VPC availability for all regions.",
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
