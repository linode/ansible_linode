#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Object Storage Quotas."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_quota_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)


def custom_api_filter_constructor(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Customize a filter string for listing Object Storage Quota,
    because only a single basic filterable parameter can be supported currently by API.
    """
    filters = params.get("filters")

    if filters is not None:
        if len(filters) == 1 and len(filters[0]["values"]) == 1:
            return {filters[0]["name"]: filters[0]["values"][0]}
        module.fail(
            "[error] The filter is not acceptable. "
            "Only a single filterable parameter can be supported currently by API. "
            "The filterable fields are limited. "
            "Please refer to the API documentation for more information."
        )

    if params.get("order_by") is not None or params.get("order") is not None:
        module.warn("[warning] order or order_by is currently not supported. "
                    "Please refer to the API documentation for more information.")

    return {}


module = ListModule(
    result_display_name="Object Storage Quotas",
    result_field_name="object_storage_quotas",
    endpoint_template="/object-storage/quotas",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-quotas",
    result_samples=docs.result_object_storage_quotas_samples,
    examples=docs.specdoc_examples,
    requires_beta=True,
    custom_api_filter_constructor=custom_api_filter_constructor,
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
