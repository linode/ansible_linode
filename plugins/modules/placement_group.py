#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Placement Groups."""


from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.placement_group as docs
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
from linode_api4 import PlacementGroup

placement_group_spec = {
    "id": SpecField(
        type=FieldType.integer,
        description="The unique ID of the placement group.",
    ),
    "label": SpecField(
        type=FieldType.string,
        description=[
            "The label of the Placement Group. "
            "This field can only contain ASCII letters, digits and dashes."
        ],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The region that the placement group is in."],
    ),
    "placement_group_type": SpecField(
        type=FieldType.string,
        description=["The type of this placement group."],
    ),
    "placement_group_policy": SpecField(
        type=FieldType.string,
        description=[
            "The policy for assigning Linodes to this placement group."
        ],
        choices=["flexible", "strict"],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage a Linode Placement Group.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=placement_group_spec,
    examples=docs.specdoc_examples,
    return_values={
        "placement_group": SpecReturnValue(
            description="The Placement Group in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-placement-group",
            type=FieldType.dict,
            sample=docs.result_placement_group_samples,
        )
    },
)

CREATE_FIELDS = {
    "label",
    "region",
    "placement_group_type",
    "placement_group_policy",
}
# Fields that can be updated on an existing placement group
MUTABLE_FIELDS = {"label"}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Placement Group"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "placement_group": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
        )

    def _get_placement_group(self) -> Optional[PlacementGroup]:
        params = self.module.params

        pg_id: int = params.get("id")
        label: str = params.get("label")

        if params.get("id"):
            try:
                return self.client.load(PlacementGroup, pg_id)
            except Exception as exception:
                return self.fail(
                    msg="failed to get placement group {0}: {1}".format(
                        pg_id, exception
                    )
                )

        try:
            return self.client.placement.groups(PlacementGroup.label == label)[
                0
            ]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get placement group {0}: {1}".format(
                    label, exception
                )
            )

    def _create_placement_group(self) -> Optional[PlacementGroup]:
        params = filter_null_values(
            {k: v for k, v in self.module.params.items() if k in CREATE_FIELDS}
        )

        try:
            return self.client.placement.group_create(**params)
        except Exception as exception:
            return self.fail(
                msg="failed to create placement group: {0}".format(exception)
            )

    def _update_placement_group(self, pg: PlacementGroup) -> None:
        # Only update the mutable field `label` when id is provided as identifier.
        if self.module.params.get("id"):
            pg._api_get()

            params = filter_null_values(self.module.params)

            handle_updates(pg, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        pg = self._get_placement_group()

        # Create the placement group if it does not already exist
        if pg is None:
            pg = self._create_placement_group()
            self.register_action("Created placement_group {0}".format(pg.id))

        self._update_placement_group(pg)

        # Force lazy-loading
        pg._api_get()

        self.results["placement_group"] = pg._raw_json

    def _handle_absent(self) -> None:
        pg = self._get_placement_group()

        if pg is not None:
            self.results["placement_group"] = pg._raw_json
            label = pg.label
            pg.delete()
            self.register_action("Deleted placement group {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Placement Group module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Placement Group module"""
    Module()


if __name__ == "__main__":
    main()
