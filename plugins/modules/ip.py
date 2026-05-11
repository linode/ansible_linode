#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module allows users to allocate or update IPv4 Addresses on their accounts."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip as docs
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
from ansible_specdoc.objects import FieldType, SpecDocMeta, SpecField, SpecReturnValue
from linode_api4 import ApiError, IPAddress

spec: dict = {
    "linode_id": SpecField(
        type=FieldType.integer,
        description=[
            "The ID of a Linode you have access to "
            "that this address will be allocated to."
        ],
    ),
    "public": SpecField(
        type=FieldType.bool,
        description=["Whether to create a public or private IPv4 address."],
    ),
    "type": SpecField(
        type=FieldType.string,
        choices=["ipv4"],
        description=[
            "The type of address you are requesting. "
            "Only IPv4 addresses may be allocated through this operation."
        ],
    ),
    "address": SpecField(
        type=FieldType.string,
        description=[
            "The IP address to update or delete.",
            "Required when updating an existing IP (e.g., promoting to reserved) "
            "or when deleting (state=absent).",
        ],
        conflicts_with=["linode_id", "public", "type"],
    ),
    "reserved": SpecField(
        type=FieldType.bool,
        description=[
            "Whether this IP address should be reserved.",
            "Setting to true promotes an existing allocated IP to a reserved IP "
            "via PUT /networking/ips/{address}.",
            "Requires the address parameter.",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this IP."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Allocates a new IPv4 Address on your Account, or updates an existing one. "
        "To allocate, the Linode must be configured to support "
        "additional addresses - "
        "please open a support ticket "
        "requesting additional addresses before attempting allocation.",
        "To promote an existing IP to reserved, provide the address and set reserved=true.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "ip": SpecReturnValue(
            description="The IP address in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-ip",
            type=FieldType.dict,
            sample=docs.result_ip_samples,
        ),
    },
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for allocating a new IP"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "ip": None,
        }
        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_together=[
                ("linode_id", "public", "type"),
            ],
        )

    def _get_ip(self, address: str) -> Optional[IPAddress]:
        try:
            ip = IPAddress(self.client, address)
            ip._api_get()
            return ip
        except ApiError as exception:
            if exception.status == 404:
                return None
            self.fail(
                msg=f"failed to get IP address {address}: {exception}",
                exception=exception,
            )
            return None
        except Exception as exception:
            self.fail(
                msg=f"failed to get IP address {address}: {exception}",
                exception=exception,
            )
            return None

    def _handle_present(self) -> None:
        params = filter_null_values(self.module.params)
        address = params.get("address")

        if address is not None:
            # Update existing IP (e.g., promote to reserved)
            ip = self._get_ip(address)
            if ip is None:
                self.fail(msg=f"IP address {address} not found")
                return

            reserved = params.get("reserved")
            if reserved is not None and ip._raw_json.get("reserved") != reserved:
                try:
                    self.client.put(
                        f"/networking/ips/{address}",
                        data={"reserved": reserved},
                    )
                    self.register_action(
                        f"Updated reserved status of IP {address} to {reserved}"
                    )
                except Exception as exc:
                    self.fail(
                        msg=f"failed to update IP {address}: {exc}"
                    )
                ip._api_get()

            self.results["ip"] = ip._raw_json
            return

        linode_id = params.get("linode_id")
        public = params.get("public")

        if linode_id is None:
            self.fail(
                msg="linode_id, public, and type are required when creating a new IP"
            )
            return

        try:
            ip = self.client.networking.ip_allocate(linode_id, public)
            self.register_action(
                f"IP allocation to Linode {linode_id} completed."
            )
        except Exception as exc:
            self.fail(msg=f"failed to allocate IP to Linode {linode_id}: {exc}")
            return

        self.results["ip"] = ip._raw_json

    def _handle_absent(self) -> None:
        # TODO: Implement deleting IP once it's available in python-sdk.
        #  Raise an error for now when user reaches deleting IP.
        self.fail(
            msg="failed to delete IP: IP deleting is currently not supported."
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for IP module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
