#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list SSH keys in their Linode profile."""

from __future__ import absolute_import, division, print_function

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

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
from linode_api4 import LinodeClient


@dataclass
class InfoModuleParam:
    display_name: str
    type: FieldType


@dataclass
class InfoModuleAttr:
    display_name: str
    type: FieldType
    get: Callable[[LinodeClient, Dict[str, Any]], Any]


@dataclass
class InfoModuleResponse:
    field: str
    field_type: FieldType
    display_name: str

    docs_url: Optional[str] = None
    samples: Optional[List[str]] = None
    get: Optional[
        Callable[[LinodeClient, Dict[str, Any], Dict[str, Any]], Any]
    ] = None


class InfoModuleBase(LinodeModuleBase):
    """A common module for listing API resources given a set of filters."""

    # The primary response attribute for this module.
    primary_response: InfoModuleResponse

    # The secondary response attributes for this module.
    # These are response fields that depend on information
    # resolved in the primary response.
    secondary_responses: List[InfoModuleResponse] = []

    # Params correspond to path IDs (e.g. linode/instances/{param1})
    # These are always required.
    params: Dict[str, InfoModuleParam] = {}

    # Attributes are fields that can independently be used to resolve
    # a resource. (i.e. label, ID).
    attributes: Dict[str, InfoModuleAttr] = {}

    # Example usages of this module.
    examples: List[str] = []

    def __init__(self) -> None:
        self.module_arg_spec = self.spec.ansible_spec
        self.results: Dict[str, Any] = {
            k: None
            for k in [
                v.field
                for v in self.secondary_responses + [self.primary_response]
            ]
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[self.attributes.keys()],
            mutually_exclusive=[self.attributes.keys()],
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for list module"""

        primary_result = None

        for k, v in self.attributes.items():
            if kwargs.get(k) is None:
                continue

            primary_result = v.get(self.client, kwargs)
            break

        if primary_result is None:
            raise ValueError("Expected a result; got None")

        self.results[self.primary_response.field] = primary_result

        for v in self.secondary_responses:
            secondary_result = v.get(self.client, primary_result, kwargs)
            self.results[v.field] = secondary_result

        return self.results

    @classmethod
    @property
    def spec(cls):
        """
        Returns the ansible-specdoc spec for this module.
        """

        options = {
            "state": SpecField(
                type=FieldType.string, required=False, doc_hide=True
            ),
            "label": SpecField(
                type=FieldType.string, required=False, doc_hide=True
            ),
        }

        for k, param in cls.params.items():
            options[k] = SpecField(
                type=param.type,
                required=True,
                description=f"The ID of the {cls.primary_response.display_name} for this resource.",
            )

        for k, attr in cls.attributes.items():
            options[k] = SpecField(
                type=attr.type,
                description=f"The {attr.display_name} of the {cls.primary_response.display_name} to resolve.",
            )

        responses = {
            v.field: SpecReturnValue(
                description=f"The returned {v.display_name}.",
                docs_url=v.docs_url,
                type=v.field_type,
                sample=v.samples,
            )
            for v in [cls.primary_response] + cls.secondary_responses
        }

        return SpecDocMeta(
            description=[
                f"Get info about a Linode {cls.primary_response.display_name}."
            ],
            requirements=global_requirements,
            author=global_authors,
            options=options,
            examples=cls.examples,
            return_values=responses,
        )
