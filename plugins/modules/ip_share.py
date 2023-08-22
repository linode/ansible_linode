#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode IP Share."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_share as ip_share_docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4.objects import Instance

ip_share_spec = {
    # Disable the default values
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "ips": SpecField(
        type=FieldType.list,
        required=True,
        description=[
            "A list of secondary Linode IPs to share with the primary Linode."
        ],
    ),
    "linode_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=[
            "The ID of the primary Linode that the addresses will be shared with."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage the Linode shared IPs."],
    requirements=global_requirements,
    author=global_authors,
    options=ip_share_spec,
    examples=ip_share_docs.specdoc_examples,
    return_values={
        "ip_share_stats": SpecReturnValue(
            description="The Linode IP share info in JSON serialized form",
            docs_url="https://www.linode.com/docs/api/networking/"
            + "#ip-addresses-share__response-samples",
            type=FieldType.dict,
            sample=ip_share_docs.result_ip_share_stats_samples,
        )
    },
)


class IPShareModule(LinodeModuleBase):
    """Module for configuring Linode shared IPs."""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "linode_id": None,
            "ips": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def _share_ip_addresses(self, ips: List[str], linode_id: str) -> None:
        """
        Configure shared IPs.
        """
        try:
            self.client.networking.ip_addresses_share(
                ips=ips,
                linode=linode_id,
            )
        except Exception as exception:
            self.fail(
                msg="failed to configure shared ips for linode {0}: {1}".format(
                    linode_id, exception
                )
            )

    # check if the IPs have been shared with the Linode instance
    def _check_shared_ip_addresses(
        self, ips: List[str], linode: Instance
    ) -> bool:
        current_ips = {i.address for i in linode.ips.ipv4.shared}

        # ensure that IPv6 ranges are only shared by checking if is_bgp is True
        for ipv6 in linode.ips.ipv6.ranges:
            # We need to make a manual GET request
            # because is_bgp is only available in the GET
            # response body.
            ipv6._api_get()

            if ipv6.is_bgp:
                current_ips.add(ipv6.range)

        return set(ips) == current_ips

    def _handle_present(self) -> None:
        linode_id = self.module.params.get("linode_id")
        ips = self.module.params.get("ips")

        linode = Instance(self.client, linode_id)

        if not self._check_shared_ip_addresses(ips, linode):
            self._share_ip_addresses(ips, linode_id)
            self.register_action("Shared IPs with Linode {0}".format(linode_id))

            linode = Instance(self.client, linode_id)
            self.results["linode_id"] = linode.id
            self.results["ips"] = [
                i.address for i in linode.ips.ipv4.shared
            ] + [i.range for i in linode.ips.ipv6.ranges]

    def _handle_absent(self) -> None:
        linode_id = self.module.params.get("linode_id")

        # Send an empty array to remove all shared IP addresses.
        self._share_ip_addresses([], linode_id)
        self.register_action(
            "Removed shared ips from Linode {0}".format(linode_id)
        )

        linode = Instance(self.client, linode_id)
        self.results["linode_id"] = linode.id
        self.results["ips"] = [i.address for i in linode.ips.ipv4.shared] + [
            i.range for i in linode.ips.ipv6.ranges
        ]

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for configuring shared IPs for a Linode."""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the IP Share module"""
    IPShareModule()


if __name__ == "__main__":
    main()
