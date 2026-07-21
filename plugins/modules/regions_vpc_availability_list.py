#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode regions VPC availability."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    regions_vpc_availability_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Regions VPC Availability",
    result_field_name="regions_vpc_availability",
    endpoint_template="/regions/vpc-availability",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-regions-vpc-availability",
    requires_beta=True,
    examples=docs.specdoc_examples,
    result_samples=docs.result_regions_vpc_availability_samples,
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
