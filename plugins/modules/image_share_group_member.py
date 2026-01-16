#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for Image Share Group Members for a Producer."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    image_share_group_member as docs,
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
from linode_api4 import ImageShareGroup, ImageShareGroupMemberToAdd

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        description=["This Image Share Group Member's unique label."],
        required=True,
    ),
    "token": SpecField(
        type=FieldType.string,
        description=[
            "A single-use Image Share Group Token provided by the Consumer. "
            "This value is required when creating a member and is never returned."
        ],
        no_log=True,
    ),
    "sharegroup_id": SpecField(
        type=FieldType.integer,
        description=["The ID of the Image Share Group this member belongs to."],
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
    description=["Manage an Image Share Group Member."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "image_share_group_member": SpecReturnValue(
            description="The Image Share Group Member in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroup-member-token",
            type=FieldType.dict,
            sample=docs.result_image_share_group_member_samples,
        ),
    },
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Image Share Group Members"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "image_share_group_member": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_if=[
                ("state", "present", ["token"]),
            ],
        )

    def _get_image_share_group_member_by_label(
        self, label: str
    ) -> Optional[Dict[str, Any]]:
        try:
            sharegroup = self.client.load(
                ImageShareGroup, self.module.params.get("sharegroup_id")
            )
            return next(
                (
                    m.__dict__
                    for m in sharegroup.get_members()
                    if m.label == label
                ),
                None,
            )
        except Exception as exception:
            return self.fail(
                msg="failed to get image share group member for label {0}: {1}".format(
                    label, exception
                )
            )

    def _create(self) -> Optional[Dict[str, Any]]:
        try:
            sharegroup = self.client.load(
                ImageShareGroup,
                self.module.params.get("sharegroup_id"),
            )

            member = ImageShareGroupMemberToAdd(
                token=self.module.params.get("token"),
                label=self.module.params.get("label"),
            )

            member_obj = sharegroup.add_member(member)
            return member_obj.__dict__

        except Exception as exception:
            return self.fail(
                msg="failed to create Image Share Group Member: {0}".format(
                    exception
                )
            )

    def _handle_present(self) -> None:
        label = self.module.params.get("label")
        member = self._get_image_share_group_member_by_label(label)

        if not member:
            member = self._create()
            self.register_action(
                "Created Image Share Group Member {0}".format(label)
            )

        self.results["image_share_group_member"] = member

    def _handle_absent(self) -> None:
        label = self.module.params.get("label")
        member = self._get_image_share_group_member_by_label(label)

        if member is None:
            return

        sharegroup = self.client.load(
            ImageShareGroup,
            self.module.params.get("sharegroup_id"),
        )

        try:
            token_uuid = member.get("token_uuid")
            sharegroup.remove_member(token_uuid=token_uuid)
            self.results["image_share_group_member"] = member
            self.register_action(f"Deleted Image Share Group Member {label}")
        except Exception as exception:
            return self.fail(
                msg="failed to delete Image Share Group Member {0}: {1}".format(
                    label, exception
                )
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Image Share Group Member module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Image Share Group Member module"""
    Module()


if __name__ == "__main__":
    main()
