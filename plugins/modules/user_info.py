#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode user."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user_info as docs
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
from linode_api4 import User

spec = {
    # Disable the default values
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "username": SpecField(
        type=FieldType.string,
        required=True,
        description=["The username of the user."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode User."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "user": SpecReturnValue(
            description="The user info in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/account/#user-view",
            type=FieldType.dict,
            sample=docs.result_user_samples,
        ),
        "grants": SpecReturnValue(
            description="The grants info in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/account/#users-grants-view__response-samples",
            type=FieldType.dict,
            sample=docs.result_grants_samples,
        ),
    },
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.required_one_of: List[str] = []
        self.results = {"user": None}

        self.module_arg_spec = SPECDOC_META.ansible_spec

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for user info module"""

        user = self.client.account.users(
            User.username == self.module.params.get("username")
        )
        grants = user.grants

        self.results["user"] = user._raw_json
        self.results["grants"] = grants._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
