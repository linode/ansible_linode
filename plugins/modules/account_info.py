#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about the current Linode account."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.account_info as docs
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

spec = {
    # Disable the default values
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode Account."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "account": SpecReturnValue(
            description="The account info in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/account/#account-view__response-samples",
            type=FieldType.dict,
            sample=docs.result_account_samples,
        )
    },
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode Account"""

    def __init__(self) -> None:
        self.required_one_of: List[str] = []
        self.results = {"account": None}

        self.module_arg_spec = SPECDOC_META.ansible_spec

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for volume info module"""

        self.results["account"] = self.client.account()._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the account_info module"""
    Module()


if __name__ == "__main__":
    main()
