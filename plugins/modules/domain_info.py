#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    create_filter_and,
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Domain

linode_domain_info_spec = {
    # We need to overwrite attributes to exclude them as requirements
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.integer,
        required=False,
        conflicts_with=["domain"],
        description=[
            "The unique domain name of the Domain.",
            "Optional if `domain` is defined.",
        ],
    ),
    "domain": SpecField(
        type=FieldType.string,
        required=False,
        conflicts_with=["id"],
        description=[
            "The unique id of the Domain.",
            "Optional if `id` is defined.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode Domain."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_domain_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "domain": SpecReturnValue(
            description="The domain in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-view",
            type=FieldType.dict,
            sample=docs_parent.result_domain_samples,
        ),
        "records": SpecReturnValue(
            description="The domain record in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-record-view",
            type=FieldType.list,
            sample=docs_parent.result_records_samples,
        ),
        "zone_file": SpecReturnValue(
            description="The zone file for the last rendered zone for the specified domain.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-zone-file-view",
            type=FieldType.list,
            sample=docs_parent.result_zone_file_samples,
        ),
    },
)

linode_domain_valid_filters = ["id", "domain"]


class LinodeDomainInfo(LinodeModuleBase):
    """Module for getting info about a Linode Domain"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {"domain": None, "records": None, "zone_file": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_matching_domain(self, spec_args: dict) -> Optional[Domain]:
        filter_items = {
            k: v
            for k, v in spec_args.items()
            if k in linode_domain_valid_filters and v is not None
        }

        filter_statement = create_filter_and(Domain, filter_items)

        try:
            # Special case because ID is not filterable
            if "id" in filter_items.keys():
                result = Domain(self.client, spec_args.get("id"))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.domains(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg="failed to get domain {0}".format(exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for domain info module"""

        domain = self._get_matching_domain(kwargs)

        if domain is None:
            self.fail("failed to get domain")

        self.results["domain"] = domain._raw_json
        self.results["records"] = paginated_list_to_json(domain.records)
        self.results["zone_file"] = self.client.get(
            "/domains/{}/zone-file".format(domain.id)
        )

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain info module"""
    LinodeDomainInfo()


if __name__ == "__main__":
    main()
