#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Tokens."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token as docs
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
from linode_api4 import PersonalAccessToken

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This token's unique label."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this token."],
    ),
    "expiry": SpecField(
        type=FieldType.string,
        default=None,
        description=["When this token should be valid until."],
    ),
    "scopes": SpecField(
        type=FieldType.string,
        description=["The OAuth scopes to create the token with."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage a Linode Token.",
        "NOTE: The full Personal Access Token is only returned "
        "when a new token has been created.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "token": SpecReturnValue(
            description="The token in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/profile/"
            "#personal-access-token-create__responses",
            type=FieldType.dict,
            sample=docs.result_token_samples,
        )
    },
)


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Tokens"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of = ["state", "label"]
        self.results = {"changed": False, "actions": [], "token": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_token_by_label(self, label: str) -> Optional[PersonalAccessToken]:
        try:
            return self.client.profile.tokens(
                PersonalAccessToken.label == label
            )[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get token {0}: {1}".format(label, exception)
            )

    def _create_token(self) -> Optional[PersonalAccessToken]:
        try:
            return self.client.profile.token_create(**self.module.params)
        except Exception as exception:
            return self.fail(
                msg="failed to create token: {0}".format(exception)
            )

    def _update_token(self, token: PersonalAccessToken) -> None:
        token._api_get()

        params = self.module.params

        if params["expiry"] and params["expiry"] != token.expiry.isoformat():
            self.fail(
                msg="failed to update token: expiry date cannot be updated"
            )

        if params["scopes"] and params["scopes"] != token.scopes:
            self.fail(msg="failed to update token: scopes cannot be updated")

    def _handle_present(self) -> None:
        params = self.module.params
        label = params.get("label")

        token = self._get_token_by_label(label)
        full_pat: Optional[str] = None

        # Create the token if it does not already exist
        if token is None:
            token = self._create_token()
            full_pat = token.token
            self.register_action("Created token {0}".format(label))

        self._update_token(token)

        # Force lazy-loading
        token._api_get()

        result_token = token._raw_json

        # If the full PAT (only returned once) is present,
        # inject it back into the result
        if full_pat is not None:
            result_token["token"] = full_pat

        self.results["token"] = token._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        token = self._get_token_by_label(label)

        if token is not None:
            self.results["token"] = token._raw_json
            token.delete()
            self.register_action("Deleted token {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Volume module"""
    Module()


if __name__ == "__main__":
    main()
