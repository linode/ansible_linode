#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    logs_destination_info as docs,
)

from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import LogsDestination

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Logs Destination",
        field_name="logs_destination",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-destination",
        samples=docs.result_logs_destination_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                LogsDestination, params.get("id")
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
