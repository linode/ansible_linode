#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domain records."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_record as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Domain, DomainRecord

linode_domain_record_spec = {
    # Unused for domain record objects
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "domain_id": SpecField(
        type=FieldType.integer, description=["The ID of the parent Domain."]
    ),
    "domain": SpecField(
        type=FieldType.string, description=["The name of the parent Domain."]
    ),
    "record_id": SpecField(
        type=FieldType.integer,
        conflicts_with=["name"],
        description=["The id of the record to modify."],
    ),
    "name": SpecField(
        type=FieldType.string,
        conflicts_with=["record_id"],
        description=[
            "The name of this Record.",
            "NOTE: If the name of the record ends with the domain, "
            "it will be dropped from the resulting record's name.",
        ],
    ),
    "port": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The port this Record points to.",
            "Only valid and required for SRV record requests.",
        ],
    ),
    "priority": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The priority of the target host for this Record.",
            "Lower values are preferred.",
            "Only valid for MX and SRV record requests.",
            "Required for SRV record requests.",
        ],
    ),
    "protocol": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The protocol this Record’s service communicates with.",
            "An underscore (_) is prepended automatically to "
            "the submitted value for this property.",
        ],
    ),
    "service": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "An underscore (_) is prepended and a period (.) "
            "is appended automatically to the submitted value for this property.",
            "Only valid and required for SRV record requests.",
            "The name of the service.",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "tag": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The tag portion of a CAA record.",
            "Only valid and required for CAA record requests.",
        ],
    ),
    "target": SpecField(
        type=FieldType.string,
        description=["The target for this Record."],
        default="",
    ),
    "ttl_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The amount of time in seconds that this Domain’s "
            "records may be cached by resolvers "
            "or other domain servers."
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        description=["The type of Record this is in the DNS system."],
    ),
    "weight": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The relative weight of this Record "
            "used in the case of identical priority."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage Linode Domain Records.",
        "NOTE: Domain records are identified by their name, target, and type.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=linode_domain_record_spec,
    examples=docs.specdoc_examples,
    return_values={
        "record": SpecReturnValue(
            description="View a single Record on this Domain.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-record-view",
            type=FieldType.dict,
            sample=docs.result_record_samples,
        )
    },
)

linode_domain_record_mutable: Set[str] = {
    "port",
    "priority",
    "protocol",
    "service",
    "tag",
    "ttl_sec",
    "weight",
}


class LinodeDomainRecord(LinodeModuleBase):
    """Module for creating and destroying Linode Domain records"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[List[str]] = [
            ["domain", "domain_id"],
            ["name", "record_id"],
        ]
        self.mutually_exclusive: List[List[str]] = [["name", "record_id"]]
        self.required_together: List[List[str]] = [["name", "type"]]
        self.results = {"changed": False, "actions": [], "record": None}

        self._domain: Optional[Domain] = None
        self._record: Optional[DomainRecord] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
            mutually_exclusive=self.mutually_exclusive,
            required_together=self.required_together,
        )

    def _find_record(
        self, domain: Domain, name: str, rtype: str, target: str
    ) -> Optional[DomainRecord]:
        # We should strip the FQDN from the user-defined record name if defined.
        suffix = "." + domain.domain
        search_name = name
        if search_name.endswith(suffix):
            search_name = search_name[: -len(suffix)]
        try:
            for record in domain.records:
                if (
                    record.name == search_name
                    and record.type == rtype
                    and record.target == target
                ):
                    return record

            return None
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get domain record {0}: {1}".format(
                    name, exception
                )
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

    def _get_record_from_params(self) -> Optional[DomainRecord]:
        params = self.module.params

        record_id = params.get("record_id")
        record_name = params.get("name")

        if record_id is not None:
            record = DomainRecord(self.client, record_id, self._domain.id)
            record._api_get()
            return record

        if record_name is not None:
            record_type = params.get("type")
            record_target = params.get("target")

            record = self._find_record(
                self._domain, record_name, record_type, record_target
            )
            return record

        return None

    def _create_record(self) -> Optional[DomainRecord]:
        params = self.module.params
        record_type = params.pop("type")
        record_name = params.get("name")

        try:
            self.register_action(
                "Created domain record {0}".format(record_name)
            )
            return self._domain.record_create(record_type, **params)
        except Exception as exception:
            return self.fail(
                msg="failed to create domain record: {0}".format(exception)
            )

    def _update_record(self) -> None:
        """Handles all update functionality for the current Domain record"""

        # Update mutable values
        should_update = False
        params = filter_null_values(self.module.params)

        for key, new_value in params.items():
            if not hasattr(self._record, key):
                continue

            if key in {"name", "record", "target"}:
                continue

            old_value = getattr(self._record, key)

            if new_value != old_value:
                if key in linode_domain_record_mutable:
                    setattr(self._record, key, new_value)
                    self.register_action(
                        'Updated Domain Record {0}: "{1}" -> "{2}"'.format(
                            key, old_value, new_value
                        )
                    )

                    should_update = True
                    continue

                self.fail(
                    "failed to update domain record {0}: {1} is a non-updatable field".format(
                        self._record.name, key
                    )
                )

        if should_update:
            self._record.save()

    def _handle_present(self) -> None:
        params = self.module.params

        self._domain = self._get_domain_from_params()
        if self._domain is None:
            return self.fail("invalid domain specified")

        record_name = params.get("name")
        record_id = params.get("record_id")

        self._record = self._get_record_from_params()

        if self._record is None and record_id is not None:
            return self.fail(
                "record with id {0} does not exist".format(record_id)
            )

        if self._record is None and record_name is not None:
            self._record = self._create_record()

        self._update_record()

        # Force lazy-loading
        self._record._api_get()

        self.results["record"] = self._record._raw_json

    def _handle_absent(self) -> None:
        self._domain = self._get_domain_from_params()
        if self._domain is None:
            return self.fail("invalid domain specified")

        self._record = self._get_record_from_params()

        if self._record is not None:
            recordid = self._record.id

            self.results["record"] = self._record._raw_json

            self._record.delete()
            self.register_action("Deleted domain record {0}".format(recordid))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Domain record module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain record module"""
    LinodeDomainRecord()


if __name__ == "__main__":
    main()
