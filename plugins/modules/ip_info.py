#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode IP address."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_info as docs
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
from linode_api4 import IPAddress

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "address": SpecField(
        type=FieldType.string,
        required=True,
        description=["The IP address to operate on."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode IP."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "ip": SpecReturnValue(
            description="The IP in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/networking/#ip-address-view__responses",
            type=FieldType.dict,
            sample=docs.result_ip_samples,
        )
    },
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"ip": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[],
            mutually_exclusive=[],
        )

    def _get_ip(self, address: str) -> IPAddress:
        try:
            ip_addr = IPAddress(self.client, address)

            ip_addr._api_get()

            return ip_addr
        except Exception as exception:
            self.fail(
                msg="failed to get IP address {0}: {1}".format(
                    address, exception
                )
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ip_info module"""

        params = filter_null_values(self.module.params)

        address = params.get("address")
        ip_addr = self._get_ip(address)

        self.results["ip"] = ip_addr._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
