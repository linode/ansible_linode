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


@dataclass
class ListModuleParam:
    """
    Represents a single parent resource ID for a list module.
    This is intended to be used for nested resources (e.g. Instance Config).
    """

    name: str
    display_name: str
    type: FieldType


class ListModule(
    LinodeModuleBase
):  # pylint: disable=too-many-instance-attributes
    """A common module for listing API resources given a set of filters."""

    def __init__(
        self,
        result_display_name: str,
        result_field_name: str,
        endpoint_template: str,
        result_docs_url: str = "",
        params: List[ListModuleParam] = None,
        examples: List[str] = None,
        result_samples: List[str] = None,
    ) -> None:
        self.result_display_name = result_display_name
        self.result_field_name = result_field_name
        self.endpoint_template = endpoint_template

        self.result_docs_url = result_docs_url
        self.params = params or []
        self.examples = examples or []
        self.result_samples = result_samples or []

        self.module_arg_spec = self.spec.ansible_spec
        self.results: Dict[str, Any] = {self.result_field_name: []}

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for list module"""

        filter_dict = construct_api_filter(self.module.params)

        self.results[self.result_field_name] = get_all_paginated(
            self.client,
            self.endpoint_template.format(**self.module.params),
            filter_dict,
            num_results=self.module.params["count"],
        )
        return self.results

    @property
    def spec(self):
        """
        Returns the ansible-specdoc spec for this module.
        """
        spec_filter = {
            "name": SpecField(
                type=FieldType.string,
                required=True,
                description=[
                    "The name of the field to filter on.",
                    f"Valid filterable fields can be found [here]({self.result_docs_url}).",
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
                description=[
                    f"The order to list {self.result_display_name}s in."
                ],
                default="asc",
                choices=["desc", "asc"],
            ),
            "order_by": SpecField(
                type=FieldType.string,
                description=[
                    f"The attribute to order {self.result_display_name}s by."
                ],
            ),
            "filters": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                suboptions=spec_filter,
                description=[
                    f"A list of filters to apply to the resulting {self.result_display_name}s."
                ],
            ),
            "count": SpecField(
                type=FieldType.integer,
                description=[
                    f"The number of {self.result_display_name}s to return.",
                    "If undefined, all results will be returned.",
                ],
            ),
        }

        # Add the parent fields to the spec
        for param in self.params:
            options[param.name] = SpecField(
                type=param.type,
                description=[
                    f"The parent {param.display_name} for this {self.result_display_name}."
                ],
                required=True,
            )

        return SpecDocMeta(
            description=[f"List and filter on {self.result_display_name}s."],
            requirements=global_requirements,
            author=global_authors,
            options=options,
            examples=self.examples,
            return_values={
                self.result_field_name: SpecReturnValue(
                    description=f"The returned {self.result_display_name}s.",
                    docs_url=self.result_docs_url,
                    type=FieldType.list,
                    elements=FieldType.dict,
                    sample=self.result_samples,
                )
            },
        )

    def run(self):
        """
        This method executes the module.
        """

        super().__init__(module_arg_spec=self.module_arg_spec)
