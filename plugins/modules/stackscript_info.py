#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode StackScript."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    stackscript as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    stackscript_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import StackScript

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.integer,
        description=["The ID of the StackScript."],
        conflicts_with=["label"],
    ),
    "label": SpecField(
        type=FieldType.string,
        description=["The label of the StackScript."],
        conflicts_with=["id"],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode StackScript."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "stackscript": SpecReturnValue(
            description="The StackScript in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/stackscripts/"
            "#stackscript-view__response-samples",
            type="dict",
            sample=docs_parent.result_stackscript_samples,
        )
    },
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode StackScript"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"stackscript": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
            mutually_exclusive=[("id", "label")],
        )

    def _get_stackscript_by_label(self, label: str) -> Optional[StackScript]:
        try:
            return self.client.linode.stackscripts(StackScript.label == label)[
                0
            ]
        except IndexError:
            return self.fail(
                msg="failed to get stackscript with label {0}: "
                "stackscript does not exist".format(label)
            )
        except Exception as exception:
            return self.fail(
                msg="failed to get stackscript {0}: {1}".format(
                    label, exception
                )
            )

    def _get_stackscript_by_id(self, stackscript_id: int) -> StackScript:
        return self._get_resource_by_id(StackScript, stackscript_id)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for stackscript_info module"""

        params = filter_null_values(self.module.params)

        if "id" in params:
            self.results["stackscript"] = self._get_stackscript_by_id(
                params.get("id")
            )._raw_json

        if "label" in params:
            self.results["stackscript"] = self._get_stackscript_by_label(
                params.get("label")
            )._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
