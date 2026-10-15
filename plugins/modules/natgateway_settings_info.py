#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about account-wide
limits, capability rules, and sizing boundaries for your NAT Gateways."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    natgateway_settings_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    mapping_to_dict,
)
from ansible_specdoc.objects import FieldType

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="NAT Gateway Settings",
        field_name="settings",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateway-settings",
        samples=docs.result_natgateway_settings_samples,
        get=lambda client, params: mapping_to_dict(
            client.networking.natgateway_settings()
        ),
    ),
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
