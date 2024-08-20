#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Firewall."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    paginated_list_to_json,
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Firewall

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="firewall",
        field_type=FieldType.dict,
        display_name="Firewall",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall",
        samples=docs_parent.result_firewall_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="devices",
            field_type=FieldType.list,
            display_name="devices",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall-devices",
            samples=docs_parent.result_devices_samples,
            get=lambda client, firewall, params: paginated_list_to_json(
                Firewall(client, firewall["id"]).devices
            ),
        ),
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Firewall,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.networking.firewalls,
                Firewall.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
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
