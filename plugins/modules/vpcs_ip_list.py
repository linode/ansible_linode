#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing IP addresses of all VPCs."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpcs_ip_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="all VPC IP Addresses",
    result_field_name="vpcs_ips",
    endpoint_template="/vpcs/ips",
    result_docs_url="",
    examples=docs.specdoc_examples,
    result_samples=docs.result_vpc_samples,
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
