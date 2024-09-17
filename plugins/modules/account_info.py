#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about the current Linode account."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.account_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Account",
        field_name="account",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-account",
        samples=docs.result_account_samples,
        get=lambda client, params: client.account()._raw_json,
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
