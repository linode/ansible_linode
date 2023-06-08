#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Domain

linode_domain_spec = {
    # Unused for domain objects
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "axfr_ips": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "The list of IPs that may perform a zone transfer for this Domain."
        ],
    ),
    "description": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The list of IPs that may perform a "
            "zone transfer for this Domain."
        ],
    ),
    "domain": SpecField(
        type=FieldType.string,
        required=True,
        description=["The domain this Domain represents."],
    ),
    "expire_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The amount of time in seconds that may pass"
            " before this Domain is no longer authoritative."
        ],
    ),
    "master_ips": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "The IP addresses representing the master DNS for this Domain."
        ],
    ),
    "refresh_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The amount of time in seconds before "
            "this Domain should be refreshed."
        ],
    ),
    "retry_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The interval, in seconds, at which a "
            "failed refresh should be retried."
        ],
    ),
    "soa_email": SpecField(
        type=FieldType.string,
        description=["The Start of Authority email address."],
        editable=True,
    ),
    "status": SpecField(
        type=FieldType.string,
        description=[
            "Used to control whether this Domain is "
            "currently being rendered."
        ],
        editable=True,
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=["An array of tags applied to this object."],
    ),
    "ttl_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The amount of time in seconds that this "
            "Domain’s records may be cached by resolvers "
            "or other domain servers."
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "Whether this Domain represents the authoritative "
            "source of information for the domain"
            " it describes (master), or whether it is a "
            "read-only copy of a master (slave)."
        ],
    ),
    # Deprecated
    "group": SpecField(type=FieldType.string, doc_hide=True),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode Domains."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_domain_spec,
    examples=docs.specdoc_examples,
    return_values={
        "domain": SpecReturnValue(
            description="The domain in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-view",
            type=FieldType.dict,
            sample=docs.result_domain_samples,
        ),
        "records": SpecReturnValue(
            description="The domain record in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-record-view",
            type=FieldType.list,
            sample=docs.result_records_samples,
        ),
        "zone_file": SpecReturnValue(
            description="The zone file for the last rendered zone for the specified domain.",
            docs_url="https://www.linode.com/docs/api/domains/#domain-zone-file-view",
            type=FieldType.list,
            sample=docs.result_zone_file_samples,
        ),
    },
)

linode_domain_mutable: Set[str] = {
    "axfr_ips",
    "description",
    "expire_sec",
    "master_ips",
    "refresh_sec",
    "retry_sec",
    "soa_email",
    "status",
    "tags",
    "ttl_sec",
    "type",
    "group",
}


class LinodeDomain(LinodeModuleBase):
    """Module for creating and destroying Linode Domains"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "domain": None,
            "zone_file": None,
        }

        self._domain: Optional[Domain] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_domain_by_name(self, name: str) -> Optional[Domain]:
        try:
            domain = self.client.domains(Domain.domain == name)[0]

            # Fix for group returning '' rather than None
            if domain.group == "":
                domain.group = None

            return domain
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get domain {0}: {1}".format(name, exception)
            )

    def _create_domain(self) -> Optional[Domain]:
        params = self.module.params
        domain = params.pop("domain")
        master = params.pop("type") == "master"

        try:
            self.register_action("Created domain {0}".format(domain))
            return self.client.domain_create(domain, master, **params)
        except Exception as exception:
            return self.fail(
                msg="failed to create domain: {0}".format(exception)
            )

    def _update_domain(self) -> None:
        """Handles all update functionality for the current Domain"""

        # Update mutable values
        should_update = False
        params = filter_null_values(self.module.params)

        for key, new_value in params.items():
            if not hasattr(self._domain, key):
                continue

            old_value = getattr(self._domain, key)

            if new_value != old_value:
                if key in linode_domain_mutable:
                    setattr(self._domain, key, new_value)
                    self.register_action(
                        'Updated Domain {0}: "{1}" -> "{2}"'.format(
                            key, old_value, new_value
                        )
                    )

                    should_update = True
                    continue

                self.fail(
                    "failed to update domain {0}: {1} is a non-updatable field".format(
                        self._domain.domain, key
                    )
                )

        if should_update:
            self._domain.save()

    def _handle_domain(self) -> None:
        params = self.module.params

        domain_name: str = params.get("domain")

        self._domain = self._get_domain_by_name(domain_name)

        # Create the domain if it does not already exist
        if self._domain is None:
            self._domain = self._create_domain()

        self._update_domain()

        # Force lazy-loading
        self._domain._api_get()

        self.results["domain"] = self._domain._raw_json
        self.results["records"] = paginated_list_to_json(self._domain.records)
        self.results["zone_file"] = self.client.get(
            "/domains/{}/zone-file".format(self._domain.id)
        )

    def _handle_domain_absent(self) -> None:
        domain_name: str = self.module.params.get("domain")

        self._domain = self._get_domain_by_name(domain_name)

        if self._domain is not None:
            self.results["domain"] = self._domain._raw_json
            self.results["records"] = paginated_list_to_json(
                self._domain.records
            )

            self._domain.delete()
            self.register_action("Deleted domain {0}".format(domain_name))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Domain module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_domain_absent()
            return self.results

        self._handle_domain()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeDomain()


if __name__ == "__main__":
    main()
