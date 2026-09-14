#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Object Storage global quotas."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_global_quota_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Object Storage Global Quotas",
    result_field_name="object_storage_global_quotas",
    endpoint_template="/object-storage/global-quotas",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-global-quotas",  # pylint: disable=line-too-long
    result_samples=docs.result_object_storage_global_quotas_samples,
    examples=docs.specdoc_examples,
    disable_filters=True,
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
