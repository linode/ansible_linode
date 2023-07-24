#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Images."""

from __future__ import absolute_import, division, print_function

import os
from typing import Any, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image as docs
import polling
import requests
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
from linode_api4 import Image

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This Image's unique label."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this Image."],
    ),
    "cloud_init": SpecField(
        type=FieldType.bool,
        description=["Whether this image supports cloud-init."],
    ),
    "description": SpecField(
        type=FieldType.string,
        editable=True,
        description=["A description for the Image."],
    ),
    "disk_id": SpecField(
        type=FieldType.integer,
        conflicts_with=["source_file"],
        description=["The ID of the disk to clone this image from."],
    ),
    "recreate": SpecField(
        type=FieldType.bool,
        default=False,
        description=[
            "If true, the image with the given label will be deleted and recreated"
        ],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The Linode region to upload this image to."],
        default="us-east",
    ),
    "source_file": SpecField(
        type=FieldType.string,
        conflicts_with=["disk_id"],
        description=["An image file to create this image with."],
    ),
    "wait": SpecField(
        type=FieldType.bool,
        default=True,
        description=[
            "Wait for the image to have status `available` before returning."
        ],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        default=600,
        description=[
            "The amount of time, in seconds, to wait for an image to "
            "have status `available`."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode Image."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "image": SpecReturnValue(
            description="The Image in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/images/"
            "#image-view__response-samples",
            type=FieldType.dict,
            sample=docs.result_image_samples,
        )
    },
)

MUTABLE_FIELDS = {"description"}


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Images"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "image": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("state", "label")],
            mutually_exclusive=[("disk_id", "source_file")],
            required_if=[
                ("state", "present", ["disk_id", "source_file"], True)
            ],
        )

    def _get_image_by_label(self, label: str) -> Optional[Image]:
        try:
            return self.client.images(Image.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get image {0}: {1}".format(label, exception)
            )

    def _wait_for_image_status(self, image: Image, status: Set[str]) -> None:
        def poll_func() -> bool:
            image._api_get()
            return image.status in status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=10,
                timeout=self._timeout_ctx.seconds_remaining,
            )
        except polling.TimeoutException:
            self.fail("failed to wait for image status: timeout period expired")

    def _create_image_from_disk(self) -> Optional[Image]:
        disk_id = self.module.params.get("disk_id")
        label = self.module.params.get("label")
        description = self.module.params.get("description")

        try:
            return self.client.image_create(
                disk_id, label=label, description=description
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create image: {0}".format(exception)
            )

    def _create_image_from_file(self) -> Optional[Image]:
        label = self.module.params.get("label")
        description = self.module.params.get("description")
        region = self.module.params.get("region")
        source_file = self.module.params.get("source_file")

        if not os.path.exists(source_file):
            return self.fail(
                msg="source file {0} does not exist".format(source_file)
            )

        # Create an image upload
        try:
            image, upload_to = self.client.images.create_upload(
                label, region, description=description
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create image upload: {0}".format(exception)
            )

        try:
            with open(source_file, "rb") as file:
                # We want to stream the image
                requests.put(
                    upload_to,
                    headers={"Content-Type": "application/octet-stream"},
                    data=file,
                )

        except Exception as exception:
            return self.fail(
                msg="failed to upload image: {0}".format(exception)
            )

        image = Image(self.client, image.id, json=image._raw_json)
        return image

    def _create_image(self) -> Optional[Image]:
        if self.module.params.get("disk_id") is not None:
            return self._create_image_from_disk()

        if self.module.params.get("source_file") is not None:
            return self._create_image_from_file()

        return self.fail(msg="no handler found for image")

    def _update_image(self, image: Image) -> None:
        image._api_get()

        params = filter_null_values(self.module.params)

        handle_updates(image, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get("label")

        image = self._get_image_by_label(label)

        if params.get("recreate") and image is not None:
            image.delete()
            self.register_action("Deleted image {0}".format(label))
            image = None

        # Create the image if it does not already exist
        if image is None:
            image = self._create_image()
            self.register_action("Created image {0}".format(label))

            if self.module.params.get("wait"):
                self._wait_for_image_status(image, {"available"})

        self._update_image(image)

        # Force lazy-loading
        image._api_get()

        self.results["image"] = image._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        image = self._get_image_by_label(label)

        if image is not None:
            self.results["image"] = image._raw_json
            image.delete()
            self.register_action("Deleted image {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Image module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Image module"""
    Module()


if __name__ == "__main__":
    main()
