#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Firewalls Settings."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_settings as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_settings_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleResult,
)
from ansible_specdoc.objects import (
    FieldType,
)
from linode_api4 import FirewallSettings

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Firewall Settings",
        field_name="firewall_settings",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall-settings",
        samples=docs_parent.result_firewall_settings_samples,
        get=lambda client, _: client.load(FirewallSettings, None)._raw_json,
    ),
    attributes=[],
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
