#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage Quota info."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_quota_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import ObjectStorageQuota

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Object Storage Quota",
        field_name="object_storage_quota",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-quota",
        samples=docs.result_object_storage_quota_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            display_name="Quota Usage",
            field_name="quota_usage",
            field_type=FieldType.dict,
            docs_url="https://techdocs.akamai.com/linode-api/reference"
            "/get-object-storage-quota-usage",
            samples=docs.result_object_storage_quota_usage_samples,
            get=lambda client, object_storage_quota, params: ObjectStorageQuota(
                client, object_storage_quota["quota_id"]
            )
            .usage()
            .dict,
        ),
    ],
    attributes=[
        InfoModuleAttr(
            name="quota_id",
            display_name="Quota ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                ObjectStorageQuota, params.get("quota_id")
            )._raw_json,
        ),
    ],
    requires_beta=True,
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
