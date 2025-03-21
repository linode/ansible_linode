#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode LKE Version."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_version_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType, SpecField
from linode_api4 import KubeVersion, LinodeClient, TieredKubeVersion


def _get_lke_version(
    client: LinodeClient, params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Retrieves the LKE version from the appropriate endpoint based on the tier parameter.

    If 'tier' is specified, it uses the TieredKubeVersion class.
    Otherwise, it uses the default KubeVersion class.
    """
    version_id = params.get("id")
    tier = params.get("tier")

    if tier:
        # If `tier` is specified, fetch the LKE version for
        # that specific tier and id (e.g., standard or enterprise)
        return client.load(TieredKubeVersion, version_id, tier)._raw_json

    # Otherwise, fetch the LKE version for the specified id
    return client.load(KubeVersion, version_id)._raw_json


module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="LKE Version",
        field_name="lke_version",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-version",
        samples=docs.result_lke_version_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.string,
            get=_get_lke_version,
        ),
    ],
    custom_options={
        "tier": SpecField(
            type=FieldType.string,
            choices=["standard", "enterprise"],
            description=[
                "Specifies the service tier for retrieving LKE version details.",
                "NOTE: LKE Enterprise may not currently be available to all users and ",
                "can only be used with v4beta.",
            ],
            required=False,
        ),
    },
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
