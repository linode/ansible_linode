#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Users."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user as docs
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
from linode_api4 import User

SPEC_GRANTS_GLOBAL = {
    "account_access": SpecField(
        type=FieldType.string,
        choices=["read_only", "read_write"],
        description=[
            "The level of access this User has to Account-level actions, "
            "like billing information.",
            "A restricted User will never be able to manage users.",
        ],
        default=None,
        editable=True,
    ),
    "add_databases": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add Managed Databases."],
        default=False,
        editable=True,
    ),
    "add_domains": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add Domains."],
        default=False,
        editable=True,
    ),
    "add_firewalls": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add Firewalls."],
        default=False,
        editable=True,
    ),
    "add_images": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add Images."],
        default=False,
        editable=True,
    ),
    "add_linodes": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add Linodes."],
        default=False,
        editable=True,
    ),
    "add_longview": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add Longview."],
        default=False,
        editable=True,
    ),
    "add_nodebalancers": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add NodeBalancers."],
        default=False,
        editable=True,
    ),
    "add_stackscripts": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add StackScripts."],
        default=False,
        editable=True,
    ),
    "add_volumes": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add Volumes."],
        default=False,
        editable=True,
    ),
    "cancel_account": SpecField(
        type=FieldType.bool,
        description=["If true, this User may add cancel the entire account."],
        default=False,
        editable=True,
    ),
    "longview_subscription": SpecField(
        type=FieldType.bool,
        description=[
            "If true, this User may manage the Account’s "
            "Longview subscription."
        ],
        default=False,
        editable=True,
    ),
}

SPEC_GRANTS_RESOURCE = {
    "type": SpecField(
        type=FieldType.string,
        choices=[
            "domain",
            "image",
            "linode",
            "longview",
            "nodebalancer",
            "stackscript",
            "volume",
            "database",
        ],
        description=["The type of resource to grant access to."],
        required=True,
        editable=True,
    ),
    "id": SpecField(
        type=FieldType.integer,
        description=["The ID of the resource to grant access to."],
        required=True,
        editable=True,
    ),
    "permissions": SpecField(
        type=FieldType.string,
        choices=["read_only", "read_write"],
        description=[
            "The level of access this User has to this entity. "
            "If null, this User has no access."
        ],
        required=True,
        editable=True,
    ),
}

SPEC_GRANTS = {
    "global": SpecField(
        type=FieldType.dict,
        description=[
            "A structure containing the Account-level grants a User has."
        ],
        suboptions=SPEC_GRANTS_GLOBAL,
        editable=True,
    ),
    "resources": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        editable=True,
        suboptions=SPEC_GRANTS_RESOURCE,
        description=["A list of resource grants to give to the user."],
    ),
}

SPEC = {
    # We don't use label for this module
    "label": SpecField(
        type=FieldType.string,
        doc_hide=True,
    ),
    "username": SpecField(
        type=FieldType.string,
        required=True,
        description=["The username of this user."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this user."],
    ),
    "restricted": SpecField(
        type=FieldType.bool,
        description=[
            "If true, the User must be granted access to perform "
            "actions or access entities on this Account."
        ],
        default=True,
        editable=True,
    ),
    "email": SpecField(
        type=FieldType.string,
        description=[
            "The email address for the User.",
            "Linode sends emails to this address for account "
            "management communications.",
            "May be used for other communications as configured.",
        ],
    ),
    "grants": SpecField(
        type=FieldType.dict,
        description=["Update the grants a user has."],
        suboptions=SPEC_GRANTS,
        editable=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode User."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "user": SpecReturnValue(
            description="The user in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/account/#user-view__response-samples",
            type=FieldType.dict,
            sample=docs.result_user_samples,
        ),
        "grants": SpecReturnValue(
            description="The grants info in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/account/"
            "#users-grants-view__response-samples",
            type=FieldType.dict,
            sample=docs.result_grants_samples,
        ),
    },
)

MUTABLE_FIELDS = {"restricted"}


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Users"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of = ["state", "username"]
        self.results = {
            "changed": False,
            "actions": [],
            "user": None,
            "grants": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
            required_if=[("state", "present", ["email"])],
        )

    @staticmethod
    def _normalize_grants_params(grants: Dict[str, Any]) -> Dict[str, Any]:
        result = {}

        if "global" in grants:
            result["global"] = grants["global"]

        if "resources" not in grants or grants["resources"] is None:
            return result

        for resource_grant in grants["resources"]:
            entity_type = resource_grant.get("type").lower()
            entity_id = resource_grant.get("id")
            permissions = resource_grant.get("permissions")

            if entity_type not in result:
                result[entity_type] = []

            result[entity_type].append(
                {"id": entity_id, "permissions": permissions}
            )

        return result

    def _get_raw_grants(self, user: User) -> Optional[Dict[Any, str]]:
        try:
            return self.client.get("/account/users/{0}/grants".format(user.id))
        except Exception as exception:
            return self.fail(
                msg="failed to get user grants: {0}".format(exception)
            )

    @staticmethod
    def _compare_grants(
        old_grants: Dict[str, Any], new_grants: Dict[str, Any]
    ) -> bool:
        normalized_grants = {"global": old_grants["global"]}

        # Remove all implicitly created values to allow for proper diffing
        resource: List[Any]

        for key, resource in old_grants.items():
            if not isinstance(resource, list):
                continue

            result_list = [
                resource_grant
                for resource_grant in resource
                if resource_grant["permissions"] is not None
            ]

            if len(result_list) > 0:
                normalized_grants[key] = result_list

        return new_grants == normalized_grants

    @staticmethod
    def _merge_grants(
        old_grants: Dict[str, Any], param_grants: Dict[str, Any]
    ) -> Dict[Any, str]:
        # This function is necessary as we want users to explicitly specify all grants that
        # should be given to a user.

        result: Dict[str, Any] = {"global": {}}

        # Set the global grant values from the params
        if param_grants["global"]:
            result["global"] = param_grants["global"]

        # Create a dict as a reference for later
        new_grant_map: Dict[str, Dict[int, Any]] = {}
        for key, resource in param_grants.items():
            if not isinstance(resource, list):
                continue

            for grant in resource:
                if key not in new_grant_map:
                    new_grant_map[key] = {}

                new_grant_map[key][grant["id"]] = grant

        # Merge the output
        for key, resource in old_grants.items():
            if not isinstance(resource, list):
                continue

            if key not in result:
                result[key] = []

            for grant in resource:
                # Use the existing grant
                if key in new_grant_map and grant["id"] in new_grant_map[key]:
                    result[key].append(new_grant_map[key][grant["id"]])
                    continue

                # Remove permissions for all other grants
                result[key].append({"id": grant["id"], "permissions": None})

        return result

    def _get_user_by_username(self, username: str) -> Optional[User]:
        try:
            return self.client.account.users(User.username == username)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get user {0}: {1}".format(username, exception)
            )

    def _create_user(self) -> Optional[User]:
        params = filter_null_values(self.module.params)
        username = params.pop("username")
        email = params.pop("email")

        for key in {"api_token", "api_version", "state", "grants", "ua_prefix"}:
            if key in params:
                params.pop(key)

        try:
            return self.client.account.user_create(email, username, **params)
        except Exception as exception:
            return self.fail(msg="failed to create user: {0}".format(exception))

    def _update_grants(self, user: User) -> None:
        params = self.module.params

        if (
            "grants" not in params
            or params["grants"] is None
            or not params["restricted"]
        ):
            return

        param_grants = self._normalize_grants_params(params["grants"])
        raw_grants = self._get_raw_grants(user)

        if self._compare_grants(raw_grants, param_grants):
            return

        # We need to merge the old grants with the new grants to properly
        # give/revoke grants declaratively
        put_body = self._merge_grants(raw_grants, param_grants)

        self.client.put(
            "/account/users/{0}/grants".format(user.id), data=put_body
        )
        self.register_action("Updated grants")

    def _update_user(self, user: User) -> None:
        user._api_get()

        params = filter_null_values(self.module.params)

        if "grants" in params:
            params.pop("grants")

        handle_updates(user, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params
        username = params.get("username")

        user = self._get_user_by_username(username)

        # Create the user if it does not already exist
        if user is None:
            user = self._create_user()
            self.register_action("Created user {0}".format(username))

        self._update_user(user)

        self._update_grants(user)

        # Force lazy-loading
        user._api_get()

        self.results["user"] = user._raw_json
        self.results["grants"] = self._get_raw_grants(user)

    def _handle_absent(self) -> None:
        username: str = self.module.params.get("username")

        user = self._get_user_by_username(username)

        if user is not None:
            self.results["user"] = user._raw_json
            self.results["grants"] = self._get_raw_grants(user)
            user.delete()
            self.register_action("Deleted user {0}".format(user.username))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode user module"""
    Module()


if __name__ == "__main__":
    main()
