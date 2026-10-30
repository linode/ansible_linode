#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list reserved IPv4 addresses on their Linode account."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.reserved_ip_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Reserved IPs",
    result_field_name="reserved_ips",
    endpoint_template="/networking/reserved/ips",
    result_docs_url=(
        "https://techdocs.akamai.com/linode-api/reference/get-reserved-ips"
    ),
    examples=docs.reserved_ip_list_specdoc_examples,
    result_samples=docs.result_reserved_ip_list_samples,
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
