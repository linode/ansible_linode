#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list SSH keys in their Linode profile."""

from __future__ import absolute_import, division, print_function

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    construct_api_filter,
    get_all_paginated,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

spec_filter = {
    "name": SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The name of the field to filter on.",
        ],
    ),
    "values": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        required=True,
        description=[
            "A list of values to allow for this field.",
            "Fields will pass this filter if at least one of these values matches.",
        ],
    ),
}


@dataclass
class ListModuleParent:
    """
    Represents a single parent resource ID for a list module.
    This is intended to be used for nested resources (e.g. Instance Config)
    """

    field: str
    display_name: str
    type: FieldType


class ListModuleBase(LinodeModuleBase):
    """A common module for listing API resources given a set of filters."""

    display_name = ""
    result_field = ""
    endpoint = ""
    docs_url = ""
    parents: List[ListModuleParent] = []
    examples = []
    response_samples = []

    def __init__(self) -> None:
        self.module_arg_spec = self.spec.ansible_spec
        self.results: Dict[str, Any] = {self.result_field: []}

        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for list module"""

        filter_dict = construct_api_filter(self.module.params)

        self.results[self.result_field] = get_all_paginated(
            self.client,
            self.endpoint.format(**self.module.params),
            filter_dict,
            num_results=self.module.params["count"],
        )
        return self.results

    @classmethod
    @property
    def spec(cls):
        """
        Returns the ansible-specdoc spec for this module.
        """
        options = {
            # Disable the default values
            "state": SpecField(
                type=FieldType.string, required=False, doc_hide=True
            ),
            "label": SpecField(
                type=FieldType.string, required=False, doc_hide=True
            ),
            "order": SpecField(
                type=FieldType.string,
                description=[f"The order to list {cls.display_name}s in."],
                default="asc",
                choices=["desc", "asc"],
            ),
            "order_by": SpecField(
                type=FieldType.string,
                description=[f"The attribute to order {cls.display_name}s by."],
            ),
            "filters": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                suboptions=spec_filter,
                description=[
                    f"A list of filters to apply to the resulting {cls.display_name}s."
                ],
            ),
            "count": SpecField(
                type=FieldType.integer,
                description=[
                    f"The number of {cls.display_name}s to return.",
                    "If undefined, all results will be returned.",
                ],
            ),
        }

        # Add the parent fields to the spec
        for parent in cls.parents:
            options[parent.field] = SpecField(
                type=parent.type,
                description=[
                    f"The parent {parent.display_name} for this {cls.display_name}"
                ],
                required=True,
            )

        return SpecDocMeta(
            description=[f"List and filter on {cls.display_name}s."],
            requirements=global_requirements,
            author=global_authors,
            options=options,
            examples=cls.examples,
            return_values={
                cls.result_field: SpecReturnValue(
                    description=f"The returned {cls.display_name}s.",
                    docs_url=cls.docs_url,
                    type=FieldType.list,
                    elements=FieldType.dict,
                    sample=cls.response_samples,
                )
            },
        )
