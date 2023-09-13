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
class ListModuleParent:
    """
    Represents a single parent resource ID for a list module.
    This is intended to be used for nested resources (e.g. Instance Config)
    """

    field: str
    display_name: str
    type: FieldType


@dataclass
class InfoModuleResponse:
    spec: SpecReturnValue
    do_request: Callable[[LinodeClient, Dict[str, Any]], Any]


@dataclass
class InfoModuleParam:
    display_name: str
    type: FieldType


@dataclass
class InfoModuleAttr:
    display_name: str
    type: FieldType
    get: Callable[[LinodeClient, Dict[str, Any]], Dict[str, Any]]


class InfoModuleBase(LinodeModuleBase):
    """A common module for listing API resources given a set of filters."""

    display_name: str
    response_field: str
    response_sample: Dict[str, Any]

    # Params correspond to path IDs (e.g. linode/instances/{param1})
    # These are always required.
    params: Dict[str, InfoModuleParam] = {}

    attributes: Dict[str, InfoModuleAttr] = {}
    examples: List[str] = []

    def __init__(self) -> None:
        self.module_arg_spec = self.spec.ansible_spec
        self.results: Dict[str, Any] = {self.response_field: None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[self.attributes.keys()],
            mutually_exclusive=[self.attributes.keys()],
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for list module"""

        result = None

        for k, v in self.attributes.items():
            if kwargs.get(k) is None:
                continue

            result = v.get(self.client, kwargs)
            break

        if result is None:
            raise ValueError("Expected a result; got None")

        self.results[self.response_field] = result

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
                description=f"The ID of the {cls.display_name} for this resource.",
            )

        for k, attr in cls.attributes.items():
            options[k] = SpecField(
                type=attr.type,
                description=f"The {attr.display_name} of the {cls.display_name} to resolve.",
            )

        return SpecDocMeta(
            description=[f"Get info about a Linode {cls.display_name}."],
            requirements=global_requirements,
            author=global_authors,
            options=options,
            examples=cls.examples,
            return_values={},
        )
