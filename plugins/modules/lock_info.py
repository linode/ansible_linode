#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode resource lock."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lock as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lock_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Lock

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="lock",
        field_type=FieldType.dict,
        display_name="Lock",
        samples=docs_parent.result_lock_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Lock, params.get("id")
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
