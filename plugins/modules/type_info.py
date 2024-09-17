#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Type."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.type_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import LinodeClient, Type


def _get_by_id(client: LinodeClient, params: Dict[str, Any]) -> None:
    """
    This function is intended to be passed into the ID get attribute.

    NOTE: This is not implemented as a lambda because Type currently does not work with
    client.load().
    """
    inst_type = Type(client, params.get("id"))
    inst_type._api_get()
    return inst_type._raw_json


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="type",
        field_type=FieldType.dict,
        display_name="Type",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-type",
        samples=docs.result_type_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.string,
            get=_get_by_id,
        )
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
