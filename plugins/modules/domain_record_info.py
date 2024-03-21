#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domain records."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    domain_record as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    domain_record_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Domain, DomainRecord

linode_domain_record_info_spec = {
    # We need to overwrite attributes to exclude them as requirements
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "domain_id": SpecField(
        type=FieldType.integer,
        conflicts_with=["domain"],
        description=[
            "The ID of the parent Domain.",
            "Optional if `domain` is defined.",
        ],
    ),
    "domain": SpecField(
        type=FieldType.string,
        conflicts_with=["domain_id"],
        description=[
            "The name of the parent Domain.",
            "Optional if `domain_id` is defined.",
        ],
    ),
    "id": SpecField(
        type=FieldType.integer,
        conflicts_with=["name"],
        description=[
            "The unique id of the subdomain.",
            "Optional if `name` is defined.",
        ],
    ),
    "name": SpecField(
        type=FieldType.string,
        conflicts_with=["id"],
        description=[
            "The name of the domain record.",
            "Optional if `id` is defined.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode Domain Record."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_domain_record_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "record": SpecReturnValue(
            description="View a single Record on this Domain.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-record-view",
            type=FieldType.dict,
            sample=docs_parent.result_record_samples,
        )
    },
)


class LinodeDomainRecordInfo(LinodeModuleBase):
    """Module for getting info about a Linode Domain record"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[List[str]] = [
            ["domain_id", "domain"],
            ["id", "name"],
        ]
        self.results: Dict[Any, Any] = {"records": []}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_domain_by_name(self, name: str) -> Optional[Domain]:
        try:
            domain = self.client.domains(Domain.domain == name)[0]
            return domain
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get domain {0}: {1}".format(name, exception)
            )

    def _get_domain_from_params(self) -> Optional[Domain]:
        domain_id = self.module.params.get("domain_id")
        domain = self.module.params.get("domain")

        if domain is not None:
            return self._get_domain_by_name(domain)

        if domain_id is not None:
            result = Domain(self.client, domain_id)
            result._api_get()
            return result

        return None

    def _get_records_by_name(
        self, domain: Domain, name: str
    ) -> Optional[List[DomainRecord]]:
        try:
            result = []

            for record in domain.records:
                if record.name == name:
                    result.append(record)

            return result
        except IndexError:
            return []
        except Exception as exception:
            return self.fail(
                msg="failed to get domain record {0}: {1}".format(
                    name, exception
                )
            )

    def _get_records_from_params(self, domain: Domain) -> List[DomainRecord]:
        record_id = self.module.params.get("id")
        record_name = self.module.params.get("name")

        if record_name is not None:
            return self._get_records_by_name(domain, record_name)

        if record_id is not None:
            result = DomainRecord(self.client, record_id, domain.id)
            result._api_get()
            return [result]

        return []

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for domain record info module"""

        domain = self._get_domain_from_params()
        if domain is None:
            return self.fail("failed to get domain")

        records = self._get_records_from_params(domain)
        if records is None:
            return self.fail("failed to get records")

        self.results["record"] = paginated_list_to_json(records)

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain Record info module"""
    LinodeDomainRecordInfo()


if __name__ == "__main__":
    main()
