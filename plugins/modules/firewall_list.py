#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing Linode Firewalls."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Firewalls",
    result_field_name="firewalls",
    endpoint_template="/networking/firewalls",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewalls",
    examples=docs.specdoc_examples,
    result_samples=docs.result_firewalls_samples,
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
