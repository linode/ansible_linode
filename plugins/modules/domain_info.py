#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file contains the implementation of the domain_info module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    paginated_list_to_json,
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Domain

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="domain",
        field_type=FieldType.dict,
        display_name="Domain",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain",
        samples=docs_parent.result_domain_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="records",
            field_type=FieldType.list,
            display_name="Records",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-records",
            samples=docs_parent.result_records_samples,
            get=lambda client, domain, params: paginated_list_to_json(
                Domain(client, domain["id"]).records
            ),
        ),
        InfoModuleResult(
            field_name="zone_file",
            field_type=FieldType.list,
            display_name="Zone File",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-zone",
            samples=docs_parent.result_zone_file_samples,
            get=lambda client, domain, params: Domain(
                client, domain["id"]
            ).zone_file_view(),
        ),
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Domain,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="domain",
            name="domain",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.domains,
                Domain.domain == params.get("domain"),
                raise_not_found=True,
            )._raw_json,
        ),
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
