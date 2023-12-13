#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Account Availability info."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    account_availability_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import AccountAvailability

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Account Availability",
        field_name="account_availability",
        field_type=FieldType.dict,
        docs_url="TBD",
        samples=docs.result_account_availability_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="region",
            display_name="Region",
            type=FieldType.string,
            get=lambda client, params: client.load(
                AccountAvailability, params.get("region")
            )._raw_json,
        ),
    ],
)

SPECDOC_META = module.spec

if __name__ == "__main__":
    module.run()
