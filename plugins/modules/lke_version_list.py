#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode LKE Versions."""

from __future__ import absolute_import, division, print_function

from typing import Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    lke_version_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)
from ansible_specdoc.objects import FieldType, SpecField


def custom_field_resolver(params: Dict[str, str]) -> Dict[str, str]:
    """
    Resolves the appropriate documentation and examples based on the 'tier' parameter.

    :param params: The parameters passed to the module.

    :returns: The appropriate documentation and examples.
    """
    if params.get("tier"):
        return {
            "endpoint_template": f"/lke/tiers/{params.get('tier')}/versions",
        }
    return {
        "endpoint_template": "/lke/versions",
    }


module = ListModule(
    result_display_name="LKE Versions",
    result_field_name="lke_versions",
    endpoint_template="/lke/versions",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-versions",
    result_samples=docs.result_lke_versions_samples,
    examples=docs.specdoc_examples,
    custom_options={
        "tier": SpecField(
            type=FieldType.string,
            choices=["standard", "enterprise"],
            description=[
                "Specifies the service tier for retrieving LKE version details.",
            ],
            required=False,
        ),
    },
    custom_field_resolver=custom_field_resolver,
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
