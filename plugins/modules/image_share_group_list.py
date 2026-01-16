#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Image Share Groups."""

from __future__ import absolute_import, division, print_function

from typing import Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    image_share_group_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)
from ansible_specdoc.objects import FieldType, SpecField


def custom_field_resolver(params: Dict[str, str]) -> Dict[str, str]:
    """
    Resolves the appropriate endpoint based on the 'image_id' parameter.

    :param params: The parameters passed to the module.

    :returns: The appropriate documentation and examples.
    """
    if params.get("image_id"):
        return {
            "endpoint_template": f"/images/{params.get('image_id')}/sharegroups",
        }
    return {
        "endpoint_template": "/images/sharegroups",
    }


module = ListModule(
    result_display_name="Image Share Groups",
    result_field_name="image_share_groups",
    endpoint_template="/images/sharegroups",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroups",
    result_samples=docs.result_image_share_groups_samples,
    examples=docs.specdoc_examples,
    custom_options={
        "image_id": SpecField(
            type=FieldType.string,
            description=[
                "Specifies the private image ID to list share groups for.",
                "If provided, only share groups containing the specified image will be returned.",
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
