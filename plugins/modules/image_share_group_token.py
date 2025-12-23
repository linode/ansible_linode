#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for Image Share Group Tokens for a Consumer."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_share_group_token as docs
from typing import Optional, Any
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
)
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
from linode_api4 import ImageShareGroupToken

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        description=["This Image Share Group Token's unique label."],
        required=True,
    ),
    "valid_for_sharegroup_uuid": SpecField(
        type=FieldType.string,
        description=["The UUID of the Image Share Group that this token is valid for."],
        required=True,
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage an Image Share Group Token."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "image_share_group_token": SpecReturnValue(
            description="The Image Share Group Token in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroup-token",
            type=FieldType.dict,
            sample=docs.result_image_share_group_token_samples,
        ),
        "single_use_token": SpecReturnValue(
            description="The single use token string to provide to a Image Share Group Producer "
                        "to be added to the share group.",
            type=FieldType.string,
            sample=docs.result_single_use_token_samples,
        )
    },
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Image Share Group Tokens"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "image_share_group_token": None,
            "single_use_token": None,
        }

        super().__init__(module_arg_spec=self.module_arg_spec)

    def _get_image_share_group_token_by_label(self, label: str) -> Optional[ImageShareGroupToken]:
        try:
            return self.client.sharegroups.tokens(ImageShareGroupToken.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get image share group token for label {0}: {1}".format(label, exception)
            )

    def _create(self) -> Optional[ImageShareGroupToken]:
        params = filter_null_values(
            {
                "label": self.module.params.get("label"),
                "valid_for_sharegroup_uuid": self.module.params.get("valid_for_sharegroup_uuid"),
            }
        )

        try:
            token_obj, single_use_token = self.client.sharegroups.create_token(**params)
            self.results["single_use_token"] = single_use_token
            return token_obj
        except Exception as exception:
            return self.fail(
                msg="failed to create Image Share Group Token: {0}".format(exception)
            )

    def _handle_present(self) -> None:
        label = self.module.params.get("label")
        token = self._get_image_share_group_token_by_label(label)

        if not token:
            token = self._create()
            self.register_action("Created Image Share Group Token {0}".format(label))

        # Force lazy-loading
        token._api_get()

        self.results["image_share_group_token"] = token._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")
        token = self._get_image_share_group_token_by_label(label)

        if token is not None:
            self.results["image_share_group_token"] = token._raw_json
            token.delete()
            self.register_action("Deleted image share group token {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Image Share Group Token module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Image Share Group Token module"""
    Module()


if __name__ == "__main__":
    main()
