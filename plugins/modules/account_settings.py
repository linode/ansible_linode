#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about the Linode account settings."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional, List

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.account_settings as docs

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
from linode_api4 import AccountSettings

SPEC = {
    "state": SpecField(
        type=FieldType.string,
        choices=["present"],
        required=True,
        description=["The state of Account Settings."],
    ),
    "backups_enabled": SpecField(
        type=FieldType.bool,
        description=[
            "Account-wide backups default. If true, all Linodes created "
            "will automatically be enrolled in the Backups service. "
            "If false, Linodes will not be enrolled by default, "
            "but may still be enrolled on creation or later."
        ],
    ),
    "interfaces_for_new_linodes": SpecField(
        type=FieldType.string,
        description=["Defines if new Linodes can use legacy configuration interfaces."],
    ),
    "longview_subscription": SpecField(
        type=FieldType.string,
        description=[
            "The Longview Pro tier you are currently subscribed to. "
            "The value must be a Longview subscription ID or null for Longview Free."
        ],
    ),
    "managed": SpecField(
        type=FieldType.bool,
        description=[
            "Our 24/7 incident response service. This robust, multi-homed "
            "monitoring system distributes monitoring checks to ensure that "
            "your servers remain online and available at all times. "
            "Linode Managed can monitor any service or software stack "
            "reachable over TCP or HTTP. Once you add a service to Linode Managed, "
            "we'll monitor it for connectivity, response, and total request time."
        ],
    ),
    "network_helper": SpecField(
        type=FieldType.bool,
        description=[
            "Enables network helper across all users by default "
            "for new Linodes and Linode Configs."
        ],
    ),
    "object_storage": SpecField(
        type=FieldType.string,
        description=[
            "A string describing the status of this account's "
            "Object Storage service enrollment."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Returns information related to your Account settings."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "account_settings": SpecReturnValue(
            description="Account Settings in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-account-settings",
            type=FieldType.dict,
            sample=docs.result_account_settings_samples,
        )
    },
)

MUTABLE_FIELDS = {"interfaces_for_new_linodes", "backups_enabled", "network_helper"}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

class Module(LinodeModuleBase):
    """Module for viewing and updating Account Settings"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "account_settings": None,
        }

        self._account_settings: Optional[AccountSettings] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _update(self) -> None:
        """Handles all updates for Account Settings"""
        handle_updates(
            self._account_settings,
            filter_null_values(self.module.params),
            MUTABLE_FIELDS,
            self.register_action,
        )

    def _present(self) -> None:
        self._account_settings = self.client.account.settings()
        self._update()
        self._account_settings._api_get()
        self.results["account_settings"] = self._account_settings._raw_json

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Account Settings module"""
        if kwargs.get("state") == "present":
            self._present()
        return self.results

if __name__ == "__main__":
    Module()
