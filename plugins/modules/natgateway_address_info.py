#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode NAT Gateway Address."""

from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    natgateway_address_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    mapping_to_dict,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import NATGateway

spec = {
    "id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The ID of the NAT Gateway."],
    ),
    "address": SpecField(
        type=FieldType.string,
        required=True,
        description=["The address to retrieve information about."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode NAT Gateway Address."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "address": SpecReturnValue(
            description="The NAT Gateway Address in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-natgateway-address",
            type=FieldType.dict,
            sample=docs.result_natgateway_address_samples,
        ),
    },
)


class Module(LinodeModuleBase):
    """Module for retrieving information about NAT Gateway Addresses"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "address": None,
        }

        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for NAT Gateway Address info module"""

        natgateway_id = self.module.params.get("id")
        address = self.module.params.get("address")

        try:
            natgateway = self.client.load(NATGateway, natgateway_id)
            address_assignment = natgateway.address_assignment_view(address)
            self.results["address"] = mapping_to_dict(address_assignment)
        except Exception as exception:
            self.fail(
                msg="failed to retrieve address {0}: {1}".format(
                    address, exception
                )
            )

        return self.results


DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

if __name__ == "__main__":
    module = Module()
    module()
