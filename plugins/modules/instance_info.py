#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Instance info."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModuleAttr,
    InfoModuleBase,
    InfoModuleResponse,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    paginated_list_to_json,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Instance


class Module(InfoModuleBase):
    """Module for getting info about a Linode Instance"""

    examples = docs.specdoc_examples

    primary_response = InfoModuleResponse(
        display_name="Instance",
        field="instance",
        field_type=FieldType.dict,
        docs_url="https://www.linode.com/docs/api/linode-instances/#linode-view__responses",
        samples=docs_parent.result_instance_samples,
    )

    secondary_responses = [
        InfoModuleResponse(
            field="configs",
            field_type=FieldType.list,
            display_name="Configs",
            docs_url="https://www.linode.com/docs/api/linode-instances/#configuration-profile-view__responses",
            samples=docs_parent.result_configs_samples,
            get=lambda client, instance, params: paginated_list_to_json(
                Instance(client, instance.get("id")).configs
            ),
        ),
        InfoModuleResponse(
            field="disks",
            field_type=FieldType.list,
            display_name="Disks",
            docs_url="https://www.linode.com/docs/api/linode-instances/#disk-view__responses",
            samples=docs_parent.result_configs_samples,
            get=lambda client, instance, params: paginated_list_to_json(
                Instance(client, instance.get("id")).disks
            ),
        ),
        InfoModuleResponse(
            field="networking",
            field_type=FieldType.dict,
            display_name="Networking Configuration",
            docs_url="https://www.linode.com/docs/api/linode-instances/#networking-information-list__responses",
            samples=docs_parent.result_configs_samples,
            get=lambda client, instance, params: client.get(
                "/linode/instances/{0}/ips".format(instance.get("id"))
            ),
        ),
    ]

    attributes = {
        "id": InfoModuleAttr(
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Instance, params.get("id")
            )._raw_json,
        ),
        "label": InfoModuleAttr(
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: client.linode.instances(
                Instance.label == params.get("label")
            )[0]._raw_json,
        ),
    }


SPECDOC_META = Module.spec

if __name__ == "__main__":
    Module()
