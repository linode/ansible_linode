#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a ACLP Monitor Service Alert Definition.
"NOTE: This module is under v4beta.","""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    alert_definition_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import AlertDefinition

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Alert Definition",
        field_name="alert_definition",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-alert-definition",
        samples=docs.result_alert_definition_samples,
    ),
    params=[
        InfoModuleParam(
            display_name="Service Type",
            name="service_type",
            type=FieldType.string,
        )
    ],
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                AlertDefinition, params.get("id"), params.get("service_type")
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
