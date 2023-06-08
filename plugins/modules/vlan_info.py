#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode VLAN info."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vlan_info as docs
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
from linode_api4 import VLAN

linode_vlan_info_spec = {
    # We need to overwrite attributes to exclude them as requirements
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(
        type=FieldType.string, required=True, description=["The VLAN’s label."]
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode VLAN."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_vlan_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "vlan": SpecReturnValue(
            description="The VLAN in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/networking/#vlans-list__response-samples",
            type=FieldType.dict,
            sample=docs.result_vlan_samples,
        )
    },
)


class LinodeVLANInfo(LinodeModuleBase):
    """Module for getting info about a Linode VLAN"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {"vlan": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_vlan_by_label(self, label: str) -> Optional[VLAN]:
        try:
            return self.client.networking.vlans(VLAN.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg="failed to get VLAN {0}".format(exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for VLAN info module"""

        label: str = kwargs.get("label")
        vlan = self._get_vlan_by_label(label)

        if vlan is None:
            self.fail("failed to get vlan")

        self.results["vlan"] = vlan._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the Linode VLAN info module"""
    LinodeVLANInfo()


if __name__ == "__main__":
    main()
