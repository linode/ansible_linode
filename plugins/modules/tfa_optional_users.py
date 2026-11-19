#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Manage the account's MFA enforcement exemptions."""

from dataclasses import asdict
from typing import Any

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    tfa_optional_users as docs,
)
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

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage the list of account users exempt from multi-factor "
        "authentication (MFA) enforcement.",
        "This module does not change the account-wide enforcement policy.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options={
        "usernames": SpecField(
            type=FieldType.list,
            element_type=FieldType.string,
            required=True,
            description=[
                "The complete list of usernames to exempt from MFA enforcement.",
                "Users not listed lose their exemption. An empty list clears "
                "all exemptions. List order does not matter.",
            ],
        ),
    },
    examples=docs.specdoc_examples,
    return_values={
        "tfa_optional_users": SpecReturnValue(
            description="The current list of exempt users.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-tfa-optional-users",
            type=FieldType.list,
            elements=FieldType.dict,
            sample=docs.result_tfa_optional_users_samples,
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
    """Reconcile the complete exemption list."""

    def __init__(self) -> None:
        self.results = {"changed": False, "actions": []}
        super().__init__(
            module_arg_spec=SPECDOC_META.ansible_spec,
        )

    def exec_module(self, **kwargs: Any) -> dict:
        """Replace the list only when membership changes."""
        account = self.client.account
        desired = set(kwargs["usernames"])
        current = list(account.tfa_optional_users())

        if desired != {user.username for user in current}:
            account.tfa_optional_users_update(sorted(desired))
            current = list(account.tfa_optional_users())
            self.register_action("Updated MFA enforcement exemptions")

        self.results["tfa_optional_users"] = [asdict(user) for user in current]
        return self.results


if __name__ == "__main__":
    Module()
