#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode rDNS."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_info as ip_docs
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_rdns as ip_rdns_docs
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
from linode_api4 import ExplicitNullValue, IPAddress

ip_rdns_spec = dict(
    # Disable the default values
    label=SpecField(type=FieldType.string, required=False, doc_hide=True),
    state=SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        description=["The state of this rDNS of the IP address."],
    ),
    address=SpecField(
        type=FieldType.string,
        description=["The IP address."],
        required=True,
    ),
    rdns=SpecField(
        type=FieldType.string,
        editable=True,
        description=["The desired rDNS value."],
    ),
)

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode IP address's rDNS."],
    requirements=global_requirements,
    author=global_authors,
    options=ip_rdns_spec,
    examples=ip_rdns_docs.specdoc_examples,
    return_values=dict(
        ip=SpecReturnValue(
            description=(
                "The updated IP address with the new "
                "reverse DNS in JSON serialized form."
            ),
            docs_url=(
                "https://www.linode.com/docs/api/profile/#ip-address-rdns-update"
            ),
            type=FieldType.dict,
            sample=ip_docs.result_ip_samples,
        )
    ),
)


class ReverseDNSModule(LinodeModuleBase):
    """Module for updating Linode IP address's reverse DNS value"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of = ["state", "rdns"]
        self.results = dict(
            changed=False,
            actions=[],
            ip=None,
        )
        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_if=[["state", "present", ["rdns"]]],
        )

    def update_rdns(self, rdns: str) -> None:
        """
        Update the reverse DNS of the IP address.
        """
        ip_str = self.module.params.get("address")
        ip_obj = self._get_resource_by_id(IPAddress, ip_str)
        ip_obj.rdns = rdns
        ip_obj.save()
        ip_obj._api_get()
        self.register_action(
            f"Updated reverse DNS of the IP address {ip_str} to be {rdns}"
        )
        self.results["ip"] = ip_obj._raw_json

    def _handle_present(self) -> None:
        rdns = self.module.params.get("rdns")
        if not rdns:
            self.fail("`rdns` attribute is required to update the IP address")
        self.update_rdns(rdns)

    def _handle_absent(self) -> None:
        self.update_rdns(ExplicitNullValue())

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for reverse DNS module"""
        state = kwargs.get("state", "present")

        if state == "absent":
            self._handle_absent()
        else:
            self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the reverse DNS module"""
    ReverseDNSModule()


if __name__ == "__main__":
    main()
