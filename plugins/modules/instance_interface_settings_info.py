#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Implementation for linode.cloud.instance_interface_settings_info module."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    instance_interface_settings as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    instance_interface_settings_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Instance

module = InfoModule(
    description=[
        "Get the interface settings for a Linode instance.",
    ],
    primary_result=InfoModuleResult(
        field_name="settings",
        field_type=FieldType.dict,
        display_name="settings",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-interface-settings",
        samples=docs_parent.result_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="Linode ID",
            name="linode_id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Instance,
                params.get("linode_id"),
            ).interfaces_settings._raw_json,
            description="The ID of the instance to retrieve the interface settings for.",
        ),
        InfoModuleAttr(
            display_name="linode_label",
            name="linode_label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.linode.instances,
                Instance.label == params.get("linode_label"),
                raise_not_found=True,
            ).interfaces_settings._raw_json,
            description="The label of the instance to retrieve the interface settings for.",
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
