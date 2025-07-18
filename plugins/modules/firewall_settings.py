#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Firewalls Settings."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_settings as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

try:
    from linode_api4 import FirewallSettings
except ImportError:
    # handled in module_utils.linode_common
    pass

default_firewall_ids_spec: dict = {
    "linode": SpecField(
        type=FieldType.integer,
        description=["The Linode's default firewall."],
    ),
    "nodebalancer": SpecField(
        type=FieldType.integer,
        description=["The NodeBalancer's default firewall."],
    ),
    "public_interface": SpecField(
        type=FieldType.integer,
        description=["The public interface's default firewall."],
    ),
    "vpc_interface": SpecField(
        type=FieldType.integer,
        description=["The VPC interface's default firewall."],
    ),
}

DEFAULT_FIREWALL_SETTING_DESCRIPTION = (
    "The default firewall ID for a `linode`, `nodebalancer`, "
    "`public_interface`, or `vpc_interface`. Default firewalls "
    "can't be deleted or disabled."
)

firewall_settings_spec: dict = {
    "default_firewall_ids": SpecField(
        type=FieldType.dict,
        suboptions=default_firewall_ids_spec,
        editable=True,
        description=[DEFAULT_FIREWALL_SETTING_DESCRIPTION],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present"],
        # Firewall settings cannot be removed.
        # Thus marking `state` field as optional here.
        required=False,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Configure the firewall settings for the account."],
    requirements=global_requirements,
    author=global_authors,
    options=firewall_settings_spec,
    examples=docs.specdoc_examples,
    return_values={
        "default_firewall_ids": SpecReturnValue(
            description=DEFAULT_FIREWALL_SETTING_DESCRIPTION,
            docs_url="https://techdocs.akamai.com/linode-api/reference/put-firewall-settings",
            type=FieldType.dict,
            sample=docs.result_firewall_settings_samples,
        ),
    },
)


DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class LinodeFirewall(LinodeModuleBase):
    """Module for creating and destroying Linode Firewalls"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec

        self.results: dict = {
            "changed": False,
            "actions": [],
            "firewall_settings": None,
        }

        self._firewall_settings: Optional[FirewallSettings] = None

        self._state = "present"

        super().__init__(module_arg_spec=self.module_arg_spec)

    def _get_firewall_settings(self) -> Optional[FirewallSettings]:
        try:
            return self.client.networking.firewall_settings()
        except Exception as exception:
            return self.fail(
                msg=f"failed to get firewall settings: {exception}"
            )

    def _update_firewall_settings(self) -> None:
        """Update the firewall settings"""

        self._firewall_settings = self._get_firewall_settings()

        handle_updates(
            self._firewall_settings,
            filter_null_values(self.module.params),
            set(["default_firewall_ids"]),
            self.register_action,
        )

        self._firewall_settings._api_get()
        self.results["firewall_settings"] = self._firewall_settings._raw_json

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Firewall Settings module"""

        self._state = self.module.params.get("state", "present")
        self._update_firewall_settings()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Firewall Settings module"""

    LinodeFirewall()


if __name__ == "__main__":
    main()
