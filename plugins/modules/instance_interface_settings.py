#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Implementation for the linode.cloud.instance_interface_settings module."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    instance_interface_settings as docs,
)
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
from linode_api4 import Instance

SPEC = {
    "instance_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=[
            "The ID of the instance to configure the interface settngs for."
        ],
    ),
    "network_helper": SpecField(
        type=FieldType.bool,
        description=[
            "Enables the Network Helper feature.",
            "The default value is determined by the network_helper setting "
            + "in the account settings.",
            "Power off the Linode before disabling or enabling Network Helper.",
        ],
    ),
    "default_route": SpecField(
        type=FieldType.dict,
        description=[
            "Interfaces used for the IPv4 default_route and IPv6 default_route when "
            "multiple interfaces are eligible for the role."
        ],
        suboptions={
            "ipv4_interface_id": SpecField(
                type=FieldType.integer,
                description=[
                    "The VPC or public interface ID assigned as the IPv4 default_route."
                ],
            ),
            "ipv6_interface_id": SpecField(
                type=FieldType.integer,
                description=[
                    "The VPC or public interface ID assigned as the IPv6 default_route."
                ],
            ),
        },
    ),
}


SPECDOC_META = SpecDocMeta(
    description=[
        "Create, read, and update the interface settings for a Linode instance.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "settings": SpecReturnValue(
            description="The Linode interface settings in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            + "get-linode-interface-settings",
            type=FieldType.dict,
            sample=docs.result_samples,
        )
    },
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode VPCS"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"changed": False, "actions": [], "settings": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token module"""
        params = self.module.params

        settings = self._get_resource_by_id(
            Instance, self.module.params.get("instance_id")
        ).interfaces_settings

        handle_updates(
            settings,
            params,
            {"network_helper", "default_route"},
            self.register_action,
            match_recursive=True,
        )

        # Force lazy-loading
        settings._api_get()

        self.results["settings"] = settings._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the Linode VPC module"""
    Module()


if __name__ == "__main__":
    main()
