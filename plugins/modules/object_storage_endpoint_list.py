#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file implements the linode.cloud.object_storage_endpoints_list module."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_endpoint_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Object Storage Endpoints",
    result_field_name="endpoints",
    endpoint_template="/object-storage/endpoints",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-endpoints",
    examples=docs.specdoc_examples,
    result_samples=docs.result_endpoints_sample,
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
