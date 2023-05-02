#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for running an API request."""

from __future__ import absolute_import, division, print_function

import ast
import contextlib

# pylint: disable=unused-import
import json
from typing import Any, Optional, Tuple

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.api_request as docs
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
from linode_api4 import ApiError

SPEC = dict(
    label=SpecField(type=FieldType.string, doc_hide=True),
    state=SpecField(type=FieldType.string, doc_hide=True),
    path=SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The relative path to the endpoint to make a request to.",
            'e.g. "linode/instances"',
        ],
    ),
    method=SpecField(
        type=FieldType.string,
        required=True,
        description=["The HTTP method of the request or response."],
        choices=["POST", "PUT", "GET", "DELETE"],
    ),
    body=SpecField(
        type=FieldType.dict,
        conflicts_with=["body_json"],
        description=[
            "The body of the request.",
            "This is a YAML structure that will be marshalled to JSON.",
        ],
    ),
    body_json=SpecField(
        type=FieldType.string,
        conflicts_with=["body"],
        description=["The body of the request in JSON format."],
    ),
    filters=SpecField(
        type=FieldType.dict,
        description=[
            "A YAML structure corresponding to the X-Filter request header.",
            "See: https://www.linode.com/docs/api/#filtering-and-sorting",
        ],
    ),
)

SPECDOC_META = SpecDocMeta(
    description=[
        "Make an arbitrary Linode API request.",
        "The Linode API documentation can be found here: "
        "https://www.linode.com/docs/api",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values=dict(
        body=SpecReturnValue(
            description="The deserialized response body.",
            type=FieldType.dict,
            sample=docs.result_body_samples,
        ),
        status=SpecReturnValue(
            description="The response status code.", type=FieldType.integer
        ),
    ),
)


class Module(LinodeModuleBase):
    """Module for running arbitrary Linode API requests"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = dict(body={}, status=0, changed=False)

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            mutually_exclusive=[("body", "body_json")],
        )

    @staticmethod
    def _parse_body_json(body_content: str) -> dict:
        with contextlib.suppress(Exception):
            # If this is a Python dict literal, parse and return
            result = ast.literal_eval(body_content)
            return result

        return json.loads(body_content)

    def do_request(
        self, method: str, path: str, filters: dict = None, body: dict = None
    ) -> Tuple[int, Optional[dict]]:
        """Runs an API request given the supplied parameters."""

        method_handlers = {
            "GET": self.client.get,
            "PUT": self.client.put,
            "POST": self.client.post,
            "DELETE": self.client.delete,
        }

        if method not in method_handlers:
            self.fail(msg="invalid request method: {}".format(method))

        try:
            return 200, method_handlers[method](
                path, filters=filters, data=body
            )
        except ApiError as err:
            return err.status, err.json

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for api_request module"""
        param_path = self.module.params.get("path")
        if not param_path.startswith("/"):
            param_path = "/" + param_path

        param_method = self.module.params.get("method")
        param_filter = self.module.params.get("filter")

        param_body = self.module.params.get("body")
        param_body_json = self.module.params.get("body_json")

        request_body = None

        if param_body is not None:
            request_body = param_body
        elif param_body_json is not None:
            request_body = self._parse_body_json(param_body_json)

        response_status, response_json = self.do_request(
            param_method, param_path, filters=param_filter, body=request_body
        )

        if response_status != 200:
            self.results["failed"] = True
        else:
            # We only want to mark as changed if the request alters a resource
            self.results["changed"] = param_method in ["PUT", "POST", "DELETE"]

        self.results["status"] = response_status
        self.results["body"] = response_json

        return self.results


def main() -> None:
    """Constructs and calls the api_request module"""
    Module()


if __name__ == "__main__":
    main()
