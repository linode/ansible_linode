#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode VPC Subnet."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_record as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_record_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleParamGroup,
    InfoModuleParamGroupPolicy,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Domain, DomainRecord, LinodeClient


def _domain_from_params(client: LinodeClient, params: Dict[str, Any]) -> Domain:
    domain_id = params.get("domain_id", None)
    domain = params.get("domain", None)

    if domain_id is not None:
        return Domain(client, domain_id)

    if domain is not None:
        target_domains = client.domains(Domain.domain == domain)
        if len(target_domains) < 1:
            raise ValueError(f"No domain with name {domain} found")

        return target_domains[0]

    raise ValueError("One of domain_id or domain must be specified")


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="record",
        field_type=FieldType.dict,
        display_name="Domain Records",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-record",
        samples=docs_parent.result_record_samples,
    ),
    params=[
        InfoModuleParamGroup(
            InfoModuleParam(
                display_name="Domain ID",
                name="domain_id",
                type=FieldType.integer,
            ),
            InfoModuleParam(
                display_name="Domain",
                name="domain",
                type=FieldType.string,
            ),
            policies=[InfoModuleParamGroupPolicy.exactly_one_of],
        )
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: [
                client.load(
                    DomainRecord,
                    params.get("id"),
                    target_parent_id=_domain_from_params(client, params).id,
                )._raw_json
            ],
        ),
        InfoModuleAttr(
            display_name="name",
            name="name",
            type=FieldType.string,
            get=lambda client, params: [
                record._raw_json
                for record in _domain_from_params(client, params).records
                if record.name == params.get("name")
            ],
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
