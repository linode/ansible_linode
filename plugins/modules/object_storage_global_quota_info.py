#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage global quota info."""

from __future__ import absolute_import, division, print_function

from typing import Any

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_global_quota_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import LinodeClient, ObjectStorageGlobalQuota


def get_quota_usage(
    client: LinodeClient,
    object_storage_global_quota: dict[str, Any],
    params: list[InfoModuleParam],
) -> dict[str, Any] | None:
    """Return quota usage details for a quota when usage is available."""
    if not object_storage_global_quota["has_usage"]:
        return None

    return (
        ObjectStorageGlobalQuota(
            client, object_storage_global_quota["quota_id"]
        )
        .usage()
        .dict
    )


module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Object Storage Global Quota",
        field_name="object_storage_global_quota",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-global-quota",
        samples=docs.result_object_storage_global_quota_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            display_name="Quota Usage",
            field_name="quota_usage",
            field_type=FieldType.dict,
            docs_url="https://techdocs.akamai.com/linode-api/reference"
            "/get-object-storage-global-quota-usage",
            samples=docs.result_object_storage_global_quota_usage_samples,
            get=get_quota_usage,
        ),
    ],
    attributes=[
        InfoModuleAttr(
            name="quota_id",
            display_name="Quota ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                ObjectStorageGlobalQuota, params.get("quota_id")
            )._raw_json,
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
