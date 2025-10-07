#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the implementation of the vpc_ipv6_list module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_ipv6_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="VPC IPv6 Addresses",
    result_field_name="addresses",
    endpoint_template="/vpcs/{vpc_id}/ipv6s",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc-ipv6s",
    examples=docs.specdoc_examples,
    result_samples=docs.result_addresses_samples,
    params=[
        ListModuleParam(
            display_name="VPC",
            name="vpc_id",
            type=FieldType.integer,
        )
    ],
    description=[
        "List and filter on all VPC IPv6 addresses for a given VPC.",
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
