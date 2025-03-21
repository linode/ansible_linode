#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list SSH keys in their Linode profile."""

from __future__ import absolute_import, division, print_function

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    BETA_DISCLAIMER,
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import LinodeClient


@dataclass
class InfoModuleParam:
    """
    Contains information about a required parameter that is necessary to resolve a resource.
    e.g. A parent resource ID.

    Attributes:
        display_name (str): The formatted name of this param for documentation purposes.
        type (FieldType): The type of this field.
    """

    name: str
    display_name: str
    type: FieldType


class InfoModuleParamGroupPolicy(Enum):
    """
    Defines the policies that can be set for a param group.
    """

    EXACTLY_ONE_OF = "exactly_one_of"


class InfoModuleParamGroup:
    """
    A base class representing a group of InfoModuleParams.
    """

    def __init__(
        self,
        *param: InfoModuleParam,
        policies: Optional[List[InfoModuleParamGroupPolicy]] = None,
    ):
        self.params = param
        self.policies = policies or set()


@dataclass
class InfoModuleAttr:
    """
    Contains information about an attribute that can be used to select a specific resource
    by property.

    Attributes:
        display_name (str): The formatted name of this attribute for documentation purposes.
        type (FieldType): The type of this field.
        get (Callable): A function to retrieve a resource from this attribute.
    """

    name: str
    display_name: str
    type: FieldType
    get: Callable[[LinodeClient, Dict[str, Any]], Any]


@dataclass
class InfoModuleResult:
    """
    Contains information about a result field returned from an info module.

    Attributes:
        field_name (str): The name of the field to be returned. (e.g. `returned_field`)
        field_type (FieldType): The type of the field to be returned.
        display_name (str): The formatted name of this field for use in documentation.
        docs_url (Optional[str]): The URL of the related API documentation for this field.
        samples (Optional[List[str]]): A list of sample results for this field.
        get (Optional[Callable]): A function to call out to the API and return the data
                                  for this field.
                                  NOTE: This is only relevant for secondary results
                                  or primary result without any attributes.
    """

    field_name: str
    field_type: FieldType
    display_name: str

    docs_url: Optional[str] = None
    samples: Optional[List[str]] = None
    get: Optional[
        Callable[[LinodeClient, Dict[str, Any], Optional[Dict[str, Any]]], Any]
    ] = None


class InfoModule(LinodeModuleBase):
    """A common module for listing API resources given a set of filters."""

    def __init__(
        self,
        primary_result: InfoModuleResult,
        secondary_results: List[InfoModuleResult] = None,
        params: Optional[
            List[Union[InfoModuleParam, InfoModuleParamGroup]]
        ] = None,
        attributes: List[InfoModuleAttr] = None,
        examples: List[str] = None,
        description: List[str] = None,
        requires_beta: bool = False,
        deprecated: bool = False,
        deprecation_message: Optional[str] = None,
        custom_options: Optional[Dict[str, SpecField]] = None,
    ) -> None:
        self.primary_result = primary_result
        self.secondary_results = secondary_results or []
        self.attributes = attributes or []
        self.examples = examples or []
        self.description = description or [
            f"Get info about a Linode {self.primary_result.display_name}."
        ]
        self.requires_beta = requires_beta
        self.deprecated = deprecated
        self.deprecation_message = (
            deprecation_message or "This module has been deprecated."
        )

        # If this module is deprecated, we should add the deprecation message
        # to the module's description.
        if self.deprecated:
            self.description.insert(0, f"**NOTE: {self.deprecation_message}**")

        # Store custom options if provided
        self.custom_options = custom_options or {}

        # Singular params should be translated into groups
        self.param_groups = [
            (
                entry
                if isinstance(entry, InfoModuleParamGroup)
                else InfoModuleParamGroup(entry)
            )
            for entry in params or []
        ]

        self.module_arg_spec = self.spec.ansible_spec
        self.results: Dict[str, Any] = {
            k: None
            for k in [
                v.field_name
                for v in self.secondary_results + [self.primary_result]
            ]
        }

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for info modules."""

        primary_result = None

        # Get the primary result using the attr get functions
        for attr in self.attributes:
            attr_value = kwargs.get(attr.name)
            if attr_value is None:
                continue

            try:
                primary_result = attr.get(self.client, kwargs)
            except Exception as exception:
                self.fail(
                    msg=f"Failed to get {self.primary_result.display_name} "
                    f"with {attr.display_name} {attr_value}: {exception}"
                )
            break

        if primary_result is None:
            # Get the primary result using the result get function
            try:
                primary_result = self.primary_result.get(self.client, kwargs)
            except Exception as exception:
                self.fail(
                    msg="Failed to get result for "
                    f"{self.primary_result.display_name}: {exception}"
                )

        if primary_result is None:
            raise ValueError("Expected a result; got None")

        self.results[self.primary_result.field_name] = primary_result

        # Pass primary result into secondary result get functions
        for attr in self.secondary_results:
            try:
                secondary_result = attr.get(self.client, primary_result, kwargs)
            except Exception as exception:
                self.fail(
                    msg=f"Failed to get {attr.display_name} for "
                    f"{self.primary_result.display_name}: {exception}"
                )
            self.results[attr.field_name] = secondary_result

        return self.results

    @property
    def spec(self):
        """
        Returns the ansible-specdoc spec for this module.
        """

        options = {}

        options.update(self.custom_options)

        # Add params to spec
        for group in self.param_groups:
            param_names = {param.name for param in group.params}

            for param in group.params:
                param_spec = SpecField(
                    type=param.type,
                    required=True,
                    description=f"The ID of the {param.display_name} for this resource.",
                )

                if InfoModuleParamGroupPolicy.EXACTLY_ONE_OF in group.policies:
                    param_spec.conflicts_with = param_names ^ {param.name}
                    param_spec.required = False

                options[param.name] = param_spec

        # Add attrs to spec
        for attr in self.attributes:
            options[attr.name] = SpecField(
                type=attr.type,
                required=len(self.attributes) == 1,
                conflicts_with=[
                    v.name for v in self.attributes if v.name != attr.name
                ],
                description=f"The {attr.display_name} of the "
                f"{self.primary_result.display_name} to resolve.",
            )

        # Add responses to spec
        responses = {
            v.field_name: SpecReturnValue(
                description=f"The returned {v.display_name}.",
                docs_url=v.docs_url,
                type=v.field_type,
                sample=v.samples,
            )
            for v in [self.primary_result] + self.secondary_results
        }

        description = self.description

        if self.requires_beta and BETA_DISCLAIMER not in description:
            description.append(BETA_DISCLAIMER)

        return SpecDocMeta(
            description=description,
            requirements=global_requirements,
            author=global_authors,
            options=options,
            examples=self.examples,
            return_values=responses,
        )

    def run(self) -> None:
        """
        Initializes and runs the info module.
        """

        if self.deprecated:
            self.warn(self.deprecation_message)

        base_module_args = {
            "module_arg_spec": self.module_arg_spec,
            "required_one_of": [],
            "mutually_exclusive": [],
        }

        attribute_names = [v.name for v in self.attributes]

        if len(attribute_names) > 0:
            base_module_args["required_one_of"].append(attribute_names)
            base_module_args["mutually_exclusive"].append(attribute_names)

        for entry in self.param_groups:
            if InfoModuleParamGroupPolicy.EXACTLY_ONE_OF in entry.policies:
                param_names = [param.name for param in entry.params]
                base_module_args["required_one_of"].append(param_names)
                base_module_args["mutually_exclusive"].append(param_names)

        super().__init__(**base_module_args)
