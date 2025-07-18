#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list all Linode firewall templates."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    firewall_template_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Firewall Templates",
    result_field_name="firewall_templates",
    endpoint_template="/networking/firewalls/templates",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall-templates",
    examples=docs.specdoc_examples,
    result_samples=docs.result_firewall_templates_samples,
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
