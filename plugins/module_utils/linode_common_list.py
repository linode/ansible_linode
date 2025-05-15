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
    BETA_DISCLAIMER,
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

    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        result_display_name: str,
        result_field_name: str,
        endpoint_template: str,
        result_docs_url: Optional[str] = None,
        params: List[ListModuleParam] = None,
        examples: List[str] = None,
        description: List[str] = None,
        result_samples: List[str] = None,
        requires_beta: bool = False,
        deprecated: bool = False,
        deprecation_message: Optional[str] = None,
        custom_options: Optional[Dict[str, SpecField]] = None,
        custom_field_resolver: Optional[callable] = None,
        custom_api_filter_constructor: Optional[callable] = None,
    ) -> None:
        self.result_display_name = result_display_name
        self.result_field_name = result_field_name
        self.endpoint_template = endpoint_template

        # Store the custom field resolver, if provided
        self.custom_field_resolver = custom_field_resolver

        # Store the custom api filter constructor, if provided
        self.custom_api_filter_constructor = custom_api_filter_constructor

        self.result_docs_url = (
            result_docs_url
            or "https://techdocs.akamai.com/linode-api/reference/api"
        )
        self.params = params or []
        self.examples = examples or []
        self.description = description or [
            f"List and filter on {self.result_display_name}."
        ]
        self.result_samples = result_samples or []
        self.requires_beta = requires_beta
        self.deprecated = deprecated
        self.deprecation_message = (
            deprecation_message or "This module has been deprecated."
        )

        # Store custom options if provided
        self.custom_options = custom_options or {}

        self.module_arg_spec = self.spec.ansible_spec
        self.results: Dict[str, Any] = {self.result_field_name: []}

        # If this module is deprecated, we should add the deprecation message
        # to the module's description.
        if self.deprecated:
            self.description.insert(0, f"**NOTE: {self.deprecation_message}**")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for list module"""

        if self.deprecated:
            self.warn(self.deprecation_message)

        # Use custom API filter constructor if provided
        filter_dict = (
            self.custom_api_filter_constructor(self.module.params)
            if self.custom_api_filter_constructor
            else construct_api_filter(self.module.params)
        )

        # Dynamically resolve fields if custom logic is provided
        if self.custom_field_resolver:
            docs = self.custom_field_resolver(self.module.params)
            self.endpoint_template = docs["endpoint_template"]

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
            "order": SpecField(
                type=FieldType.string,
                description=[
                    f"The order to list {self.result_display_name} in."
                ],
                default="asc",
                choices=["desc", "asc"],
            ),
            "order_by": SpecField(
                type=FieldType.string,
                description=[
                    f"The attribute to order {self.result_display_name} by."
                ],
            ),
            "filters": SpecField(
                type=FieldType.list,
                element_type=FieldType.dict,
                suboptions=spec_filter,
                description=[
                    f"A list of filters to apply to the resulting {self.result_display_name}."
                ],
            ),
            "count": SpecField(
                type=FieldType.integer,
                description=[
                    f"The number of {self.result_display_name} to return.",
                    "If undefined, all results will be returned.",
                ],
            ),
        }

        options.update(self.custom_options)

        # Add the parent fields to the spec
        for param in self.params:
            options[param.name] = SpecField(
                type=param.type,
                description=[
                    f"The parent {param.display_name} for the {self.result_display_name}."
                ],
                required=True,
            )

        description = self.description

        if self.requires_beta and BETA_DISCLAIMER not in description:
            description.append(BETA_DISCLAIMER)

        return SpecDocMeta(
            description=description,
            requirements=global_requirements,
            author=global_authors,
            options=options,
            examples=self.examples,
            return_values={
                self.result_field_name: SpecReturnValue(
                    description=f"The returned {self.result_display_name}.",
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
