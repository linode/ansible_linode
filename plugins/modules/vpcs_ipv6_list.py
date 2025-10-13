#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the implementation of the vpcs_ipv6_list module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpcs_ipv6_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="all VPC IPv6 Addresses",
    result_field_name="addresses",
    endpoint_template="/vpcs/ipv6s",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpcs-ipv6s",
    examples=docs.specdoc_examples,
    result_samples=docs.result_addresses_samples,
    description=[
        "List and filter on all VPC IPv6 addresses.",
        "NOTE: IPv6 VPCs may not currently be available to all users.",
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
