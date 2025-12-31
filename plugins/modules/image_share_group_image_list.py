#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Image Share Group Images."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    image_share_group_image_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="Image Share Group Images",
    result_field_name="image_share_group_images",
    endpoint_template="/images/sharegroups/{sharegroup_id}/images",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroup-images",
    result_samples=docs.result_image_share_group_images_samples,
    examples=docs.specdoc_examples,
    params=[
        ListModuleParam(
            display_name="Image Share Group",
            name="sharegroup_id",
            type=FieldType.integer,
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
