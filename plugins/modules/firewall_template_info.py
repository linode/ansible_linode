#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode firewall template."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    firewall_template_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import (
    FieldType,
)
from linode_api4 import FirewallTemplate

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Firewall Template",
        field_name="firewall_template",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall-template",
        samples=docs.result_firewall_template_samples,
        get=lambda client, _: client.load(FirewallTemplate, None)._raw_json,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="Slug",
            name="slug",
            type=FieldType.string,
            get=lambda client, params: client.load(
                FirewallTemplate,
                params.get("slug"),
            )._raw_json,
        ),
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
