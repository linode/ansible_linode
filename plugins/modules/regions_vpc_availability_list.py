#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode regions VPC availability."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.regions_vpc_availability_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Regions VPC Availability",
    result_field_name="regions_vpc_availability",
    endpoint_template="/regions/vpc-availability",
    result_docs_url="TODO",
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
