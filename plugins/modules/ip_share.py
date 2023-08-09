#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode IP Share."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

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
        self.results = {"ip_share": None}
        self._state = "present"
        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def _share_ip_addresses(self) -> None:
        """
        Configure shared IPs.
        """
        try:
            return self.client.networking.ip_addresses_share(
                ips=self.module.params.get("ips"),
                linode=self.module.params.get("linode_id"),
            )
        except Exception as exception:
            return self.fail(
                msg="failed to configure shared ips for linode {0}: {1}".format(
                    self.module.params.get("linode_id"), exception
                )
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for configuring shared IPs for a Linode."""
        linode_id = self.module.params.get("linode_id")

        self._share_ip_addresses()

        linode = Instance(self.client, linode_id)

        self.results["linode_id"] = linode_id
        self.results["ips"] = [
            s.address for s in linode.ips.ipv4.shared
        ] + linode.ips.ipv6.ranges

        return self.results


def main() -> None:
    """Constructs and calls the IP Share module"""
    IPShareModule()


if __name__ == "__main__":
    main()
