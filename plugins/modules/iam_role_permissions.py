#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode IAM role permissions."""

from typing import Any, Dict, List, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    iam_role_permissions as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    BETA_DISCLAIMER,
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

entity_access_spec: dict = {
    "id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The ID of the entity."],
    ),
    "type": SpecField(
        type=FieldType.string,
        required=True,
        description=["The type of the entity (e.g. `linode`, `firewall`)."],
    ),
    "roles": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        required=True,
        description=["The roles the user has on the entity."],
    ),
}

iam_role_permissions_spec: dict = {
    "username": SpecField(
        type=FieldType.string,
        required=True,
        description=["The username of the user to assign roles to."],
    ),
    "account_access": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "The account-level roles to assign to the user.",
            "If omitted, the user's current account-level roles are preserved.",
        ],
    ),
    "entity_access": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=entity_access_spec,
        editable=True,
        description=[
            "The entity-level roles to assign to the user.",
            "If omitted, the user's current entity-level roles are preserved.",
            "Specify an empty list to remove all entity-level roles.",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present"],
        # Role permissions cannot be removed, only replaced.
        required=False,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Update the roles assigned to a user.",
        "The specified roles replace the user's existing roles.",
        BETA_DISCLAIMER,
    ],
    requirements=global_requirements,
    author=global_authors,
    options=iam_role_permissions_spec,
    examples=docs.specdoc_examples,
    return_values={
        "role_permissions": SpecReturnValue(
            description="The user's role permissions.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/put-user-role-permissions",
            type=FieldType.dict,
            sample=docs.result_role_permissions_samples,
        ),
    },
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


def normalize_account_access(roles: Optional[List[str]]) -> List[str]:
    """Returns a sorted, de-duplicated copy of the given account roles."""
    return sorted(set(roles or []))


def normalize_entity_access(
    entries: Optional[List[Dict[str, Any]]],
) -> Dict[tuple, List[str]]:
    """
    Converts entity access entries into a mapping of (type, id) to sorted roles
    so that two lists can be compared regardless of ordering.
    """
    result: Dict[tuple, List[str]] = {}

    for entry in entries or []:
        key = (entry["type"], int(entry["id"]))
        result[key] = sorted(set(result.get(key, [])) | set(entry["roles"]))

    return result


class Module(LinodeModuleBase):
    """Module for updating Linode IAM role permissions"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec

        self.results: dict = {
            "changed": False,
            "actions": [],
            "role_permissions": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            supports_check_mode=True,
        )

    def _get_current(self, username: str) -> dict:
        try:
            return self.client.iam.role_permissions_user_get(username)
        except Exception as exception:
            return self.fail(
                msg=f"failed to get role permissions for {username}: "
                f"{exception}"
            )

    def _update(self) -> None:
        params = self.module.params
        username = params["username"]
        desired_account = params.get("account_access")
        desired_entity = params.get("entity_access")

        current = self._get_current(username)
        self.results["role_permissions"] = current

        current_account = current.get("account_access") or []
        current_entity = current.get("entity_access") or []

        account_changed = desired_account is not None and (
            normalize_account_access(desired_account)
            != normalize_account_access(current_account)
        )
        entity_changed = desired_entity is not None and (
            normalize_entity_access(desired_entity)
            != normalize_entity_access(current_entity)
        )

        if not account_changed and not entity_changed:
            return

        if account_changed:
            self.register_action(f"Update account_access for user {username}")

        if entity_changed:
            self.register_action(f"Update entity_access for user {username}")

        if self.module.check_mode:
            return

        # The API replaces the full set of roles, so unspecified
        # fields must be carried over from the current state.
        try:
            self.results["role_permissions"] = (
                self.client.iam.role_permissions_user_set(
                    username,
                    account_access=(
                        desired_account
                        if desired_account is not None
                        else current_account
                    ),
                    entity_access=(
                        desired_entity
                        if desired_entity is not None
                        else current_entity
                    ),
                )
            )
        except Exception as exception:
            self.fail(
                msg=f"failed to update role permissions for {username}: "
                f"{exception}"
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for the IAM role permissions module"""

        self._update()

        return self.results


def main() -> None:
    """Constructs and calls the IAM role permissions module"""

    Module()


if __name__ == "__main__":
    main()
