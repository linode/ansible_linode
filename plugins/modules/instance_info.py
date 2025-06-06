#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Instance info."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance_info as docs
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
from linode_api4 import Instance

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Instance",
        field_name="instance",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-instance",
        samples=docs_parent.result_instance_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="configs",
            field_type=FieldType.list,
            display_name="Configs",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-config",
            samples=docs_parent.result_configs_samples,
            get=lambda client, instance, params: paginated_list_to_json(
                Instance(client, instance.get("id")).configs
            ),
        ),
        InfoModuleResult(
            field_name="disks",
            field_type=FieldType.list,
            display_name="Disks",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-disk",
            samples=docs_parent.result_disks_samples,
            get=lambda client, instance, params: paginated_list_to_json(
                Instance(client, instance.get("id")).disks
            ),
        ),
        InfoModuleResult(
            field_name="networking",
            field_type=FieldType.dict,
            display_name="Networking Configuration",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-ips",
            samples=docs_parent.result_networking_samples,
            get=lambda client, instance, params: client.get(
                "/linode/instances/{0}/ips".format(instance.get("id"))
            ),
        ),
        InfoModuleResult(
            field_name="linode_interfaces",
            field_type=FieldType.list,
            display_name="Linode Interfaces",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-interfaces",
            samples=docs_parent.result_linode_interfaces_samples,
            get=lambda client, instance, params: client.get(
                "/linode/instances/{0}/interfaces".format(instance.get("id"))
            ),
        ),
    ],
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Instance, params.get("id")
            )._raw_json,
        ),
        InfoModuleAttr(
            name="label",
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.linode.instances,
                Instance.label == params.get("label"),
                raise_not_found=True,
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
