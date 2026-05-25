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
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ApiError, IPAddress, ReservedIPAddress

spec: dict = {
    "linode_id": SpecField(
        type=FieldType.integer,
        description=[
            "The ID of a Linode you have access to ",
            "that this address will be allocated to.",
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
            "The type of address you are requesting. ",
            "Only IPv4 addresses may be allocated through this operation.",
        ],
    ),
    "address": SpecField(
        type=FieldType.string,
        description=[
            "The IP address to update or delete.",
            "Required when updating an existing IP (e.g., promoting to reserved) ",
            "or when deleting (state=absent).",
        ],
        conflicts_with=["linode_id", "public", "type"],
    ),
    "reserved": SpecField(
        type=FieldType.bool,
        description=[
            "Whether this IP address should be reserved.",
            "Setting to true promotes an existing allocated IP to a reserved IP ",
            "via PUT /networking/ips/{address}.",
            "Requires the address parameter.",
        ],
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "Tags to apply to this IP address.",
            "NOTE: Tags are replaced entirely on update, not appended.",
            "Only applicable when updating an existing IP via the address parameter.",
        ],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=[
            "The region in which to allocate a new reserved IP address.",
            "Required when allocating a new reserved IP (reserved=true) without ",
            "specifying an existing address.",
        ],
        conflicts_with=["linode_id", "public", "address"],
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
        "Allocates a new IPv4 Address on your Account, or updates an existing one. ",
        "To allocate, the Linode must be configured to support ",
        "additional addresses - ",
        "please open a support ticket ",
        "requesting additional addresses before attempting allocation.",
        "To allocate a new reserved IP, provide region, type, and set reserved=true.",
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
                ("linode_id", "public"),
            ],
            required_if=[
                ("reserved", True, ["address", "region"], True),
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

    def _update_tags(self, address: str, ip: IPAddress) -> Optional[list]:
        """Update tags for an IP via the reserved-IPs endpoint.

        Returns the current tags list, or None if tags were not requested.
        Tags can only be managed on reserved IPs.
        """
        new_tags = self.module.params.get("tags")
        if new_tags is None:
            return None

        try:
            reserved_ip = ReservedIPAddress(self.client, address)
            reserved_ip._api_get()
            old_tags = list(reserved_ip.tags or [])
        except ApiError as exc:
            if exc.status == 404:
                self.fail(
                    msg=f"tags can only be set on reserved IPs; "
                    f"{address} is not a reserved IP"
                )
                return None
            self.fail(msg=f"failed to fetch tags for IP {address}: {exc}")
            return None

        if set(new_tags) == set(old_tags):
            return old_tags

        try:
            self.client.put(
                f"/networking/reserved/ips/{address}",
                data={"tags": new_tags},
            )
            self.register_action(f'Updated tags: "{old_tags}" -> "{new_tags}"')
            self.results["changed"] = True
        except Exception as exc:
            self.fail(msg=f"failed to update tags for IP {address}: {exc}")

        return new_tags

    def _handle_update_existing_ip(self, address: str, params: dict) -> None:
        """Handle updates to an existing IP (reserved promotion and tags)."""
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
                self.fail(msg=f"failed to update IP {address}: {exc}")
            ip._api_get()

        current_tags = self._update_tags(address, ip)
        ip_data: dict = ip._raw_json
        if current_tags is not None:
            ip_data["tags"] = current_tags
        self.results["ip"] = ip_data

    def _handle_present(self) -> None:
        params = filter_null_values(self.module.params)
        address = params.get("address")
        tags = params.get("tags")
        region = params.get("region")
        reserved = params.get("reserved")

        if tags is not None and address is None:
            self.fail(msg="tags requires address to be specified")

        if region is not None and not reserved:
            self.fail(msg="region is only valid when reserved=true")

        if address is not None:
            self._handle_update_existing_ip(address, params)
            return

        linode_id = params.get("linode_id")
        public = params.get("public")

        if region is not None and reserved:
            # Allocate a new reserved IP via POST /networking/ips
            ip_type = params.get("type", "ipv4")
            try:
                result = self.client.post(
                    "/networking/ips",
                    data={
                        "type": ip_type,
                        "public": True,
                        "region": region,
                        "reserved": True,
                    },
                )
                self.register_action(
                    f"Allocated new reserved IP in region {region}."
                )
            except Exception as exc:
                self.fail(
                    msg=f"failed to allocate reserved IP in region {region}: {exc}"
                )

            self.results["ip"] = result
            return

        if linode_id is None or public is None:
            self.fail(
                msg="linode_id and public are required when creating a new IP"
            )

        try:
            ip = self.client.networking.ip_allocate(linode_id, public)
            self.register_action(
                f"IP allocation to Linode {linode_id} completed."
            )
        except Exception as exc:
            self.fail(msg=f"failed to allocate IP to Linode {linode_id}: {exc}")

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
