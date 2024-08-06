#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for Linode Placement Group Assignment."""


from __future__ import absolute_import, division, print_function

from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    placement_group_assign as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import FieldType, SpecDocMeta, SpecField
from linode_api4 import PlacementGroup

placement_group_assignment_spec = {
    # Disable the default values
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "placement_group_id": SpecField(
        type=FieldType.integer,
        required=True,
        description="The ID of the Placement Group for this assignment.",
    ),
    "linode_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=[
            "The Linode ID to assign or unassign to the Placement Group."
        ],
    ),
    "compliant_only": SpecField(
        type=FieldType.bool,
        description=[],
        doc_hide=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manages a single assignment between a Linode and a Placement Group.",
        "NOTE: Placement Groups may not currently be available to all users.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=placement_group_assignment_spec,
    examples=docs.specdoc_examples,
    return_values={},
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Placement Group Assignment"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def _get_placement_group(self) -> Optional[PlacementGroup]:
        pg_id: int = self.module.params.get("placement_group_id")

        try:
            return self.client.load(PlacementGroup, pg_id)
        except Exception as exception:
            return self.fail(
                msg="failed to get placement group {0}: {1}".format(
                    pg_id, exception
                )
            )

    def _handle_present(self) -> None:
        """
        Assign a Linode to a placement group.
        """
        pg = self._get_placement_group()
        linode: int = self.module.params.get("linode_id")

        pg.assign([linode], self.module.params.get("compliant_only"))

        self.register_action(
            "Assign linode {0} to placement group {1}".format(linode, pg.id)
        )

    def _handle_absent(self) -> None:
        """
        Unassign a Linode from a placement group.
        """
        pg = self._get_placement_group()
        linode: int = self.module.params.get("linode_id")

        pg.unassign([linode])

        self.register_action(
            "Unassign linode {0} from placement group {1}".format(linode, pg.id)
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Placement Group Assignment module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Placement Group Assignment module"""
    Module()


if __name__ == "__main__":
    main()
