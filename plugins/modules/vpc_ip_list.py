#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing IP addresses of a VPC."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_ip_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="VPC IP Addresses",
    result_field_name="vpcs_ips",
    endpoint_template="/vpcs/{vpc_id}/ips",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc-ips",
    examples=docs.specdoc_examples,
    result_samples=docs.result_vpc_ip_view_samples,
    params=[
        ListModuleParam(
            display_name="VPC",
            name="vpc_id",
            type=FieldType.integer,
        )
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
