#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module allows users to manage reserved IPv4 addresses."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.reserved_ip as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    handle_updates,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ApiError, ReservedIPAddress

reserved_ip_spec = {
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this reserved IP address."],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=[
            "The Region in which to reserve the IP address.",
            "Required when creating a new reservation (state=present without an existing address).",
        ],
    ),
    "address": SpecField(
        type=FieldType.string,
        description=[
            "The reserved IPv4 address.",
            "Required when deleting (state=absent) or updating an existing reserved IP.",
        ],
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "Tags to apply to this reserved IP address.",
            "NOTE: Tags are replaced entirely on update, not appended.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage a Linode Reserved IPv4 Address.",
        "NOTE: Reserved IP feature may not currently be available to all users.",
        "NOTE: When creating a reservation by region (without specifying an address), "
        "this module is NOT idempotent — each run will allocate a new billable reserved "
        "IP address. To manage an existing reservation idempotently, "
        "specify the address parameter.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=reserved_ip_spec,
    examples=docs.specdoc_examples,
    return_values={
        "reserved_ip": SpecReturnValue(
            description="The reserved IP address in JSON serialized form.",
            docs_url=(
                "https://techdocs.akamai.com/linode-api/reference/get-reserved-ip"
            ),
            type=FieldType.dict,
            sample=docs.result_reserved_ip_samples,
        ),
    },
)

MUTABLE_FIELDS: Set[str] = {"tags"}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class ReservedIPModule(LinodeModuleBase):
    """Module for managing reserved IPv4 addresses"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "reserved_ip": None,
        }
        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_if=[
                ["state", "absent", ["address"]],
            ],
        )

    def _get_reserved_ip(self, address: str) -> Optional[ReservedIPAddress]:
        try:
            ip = ReservedIPAddress(self.client, address)
            ip._api_get()
            return ip
        except ApiError as exception:
            if exception.status == 404:
                return None
            self.fail(
                msg="failed to get reserved IP address {0}: {1}".format(
                    address, exception
                ),
                exception=exception,
            )
            return None
        except Exception as exception:
            self.fail(
                msg="failed to get reserved IP address {0}: {1}".format(
                    address, exception
                ),
                exception=exception,
            )
            return None

    def _create_reserved_ip(self) -> Optional[ReservedIPAddress]:
        params = self.module.params
        region = params.get("region")
        tags = params.get("tags")

        if region is None:
            return self.fail(
                msg="region is required when creating a new reserved IP"
            )

        try:
            create_kwargs = {"region": region}
            if tags is not None:
                create_kwargs["tags"] = tags
            return self.client.networking.reserved_ip_create(**create_kwargs)
        except Exception as exception:
            return self.fail(msg=f"failed to create reserved IP: {exception}")

    def _handle_present(self) -> None:
        address = self.module.params.get("address")

        reserved_ip = None
        if address is not None:
            reserved_ip = self._get_reserved_ip(address)

        if reserved_ip is None and address is not None:
            self.fail(msg=f"reserved IP {address} not found")
            return

        if reserved_ip is None:
            reserved_ip = self._create_reserved_ip()
            self.register_action(f"Created reserved IP {reserved_ip.address}")

        handle_updates(
            reserved_ip,
            self.module.params,
            MUTABLE_FIELDS,
            self.register_action,
        )

        reserved_ip._api_get()
        self.results["reserved_ip"] = reserved_ip._raw_json

    def _handle_absent(self) -> None:
        address = self.module.params.get("address")

        reserved_ip = self._get_reserved_ip(address)

        if reserved_ip is not None:
            self.results["reserved_ip"] = reserved_ip._raw_json
            try:
                reserved_ip.delete()
            except Exception as exception:
                self.fail(
                    msg=f"failed to delete reserved IP {address}: {exception}"
                )
            self.register_action(f"Deleted reserved IP {address}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for reserved_ip module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()
        return self.results


def main() -> None:
    """Constructs and calls the reserved IP module"""
    ReservedIPModule()


if __name__ == "__main__":
    main()
