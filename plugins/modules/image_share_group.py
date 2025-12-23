#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for Image Share Groups for a Producer."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_share_group as docs
import copy
from typing import Any, Optional
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values_recursive,
    handle_updates,
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
from linode_api4 import ImageShareGroup, ImageShareGroupImageToAdd, ImageShareGroupImagesToAdd, \
    ImageShareGroupImageToUpdate

image_share_group_images_spec = {
    "id": SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The id of the Private Image to include in an Image Share Group."
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        description=[
            "A label to assign to the Image within the context of an Image Share Group."
        ],
    ),
    "description": SpecField(
        type=FieldType.string,
        description=[
            "A description to assign to the Image within the context of an Image Share Group."
        ],
    ),
}

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        description=["This Image Share Group's unique label."],
        required=True,
    ),
    "description": SpecField(
        type=FieldType.string,
        description=["A description of this Image Share Group."],
    ),
    "images": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=image_share_group_images_spec,
        description=["A list of images to include in this Image Share Group."],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage an Image Share Group."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "image_share_group": SpecReturnValue(
            description="The Image Share Group in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-sharegroup",
            type=FieldType.dict,
            sample=docs.result_image_share_group_samples,
        )
    },
)

MUTABLE_FIELDS = {"description"}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Image Share Groups"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "image_share_group": None,
        }

        super().__init__(module_arg_spec=self.module_arg_spec)

    def _get_image_share_group_by_label(self, label: str) -> Optional[ImageShareGroup]:
        try:
            return self.client.sharegroups(ImageShareGroup.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get image share group {0}: {1}".format(label, exception)
            )

    def _create(self) -> Optional[ImageShareGroup]:
        params = filter_null_values_recursive(
            {
                "label": self.module.params.get("label"),
                "description": self.module.params.get("description"),
                "images": self.module.params.get("images"),
            }
        )

        try:
            return self.client.sharegroups.create_sharegroup(**params)
        except Exception as exception:
            return self.fail(
                msg="failed to create Image Share Group: {0}".format(exception)
            )

    def _update(self, image_share_group: ImageShareGroup) -> Optional[ImageShareGroup]:
        image_share_group._api_get()

        new_params = filter_null_values_recursive(copy.deepcopy(self.module.params))
        new_params = {k: v for k, v in new_params.items() if k in MUTABLE_FIELDS}

        images_to_update = self.module.params.get("images")

        handle_updates(
            image_share_group, new_params, MUTABLE_FIELDS, self.register_action
        )

        # Only touch images if explicitly provided
        if images_to_update is not None:
            self._update_images(image_share_group, images_to_update)

        return image_share_group

    def _update_images(self, image_share_group: ImageShareGroup, desired_images: list) -> None:
        desired_images = desired_images or []

        # Build a map of the desired state of images by their private IDs
        plan_map = {
            img["id"]: img
            for img in desired_images
        }

        # Build a map of the remote state of images by their private IDs
        remote_map = {}
        for img in image_share_group.get_image_shares():
            shared_by = getattr(
                getattr(img, "image_sharing", None),
                "shared_by",
                None,
            )
            private_id = getattr(shared_by, "source_image_id", None)
            if not private_id:
                continue

            remote_map[private_id] = {
                "shared_id": getattr(img, "id", None),
                "label": getattr(img, "label", None),
                "description": getattr(img, "description", None),
            }

        to_add = []
        to_update = []
        to_remove = []

        # Determine which images to add and update
        for private_id, desired_image in plan_map.items():
            remote = remote_map.get(private_id)

            if not remote:
                # Not present remotely, should be added
                to_add.append({
                    "id": private_id,
                    "label": desired_image.get("label"),
                    "description": desired_image.get("description"),
                })
                continue

            # Present remotely, check if an update is needed
            label_changed = desired_image.get("label") != remote.get("label")
            desc_changed = desired_image.get("description") != remote.get("description")

            if label_changed or desc_changed:
                opts = {}
                if label_changed:
                    opts["label"] = desired_image.get("label")
                if desc_changed:
                    opts["description"] = desired_image.get("description")

                to_update.append({
                    "shared_id": remote["shared_id"],
                    "opts": opts,
                })

        # Determine which images to remove
        for private_id, remote in remote_map.items():
            if private_id not in plan_map:
                to_remove.append(remote["shared_id"])

        # Add
        if to_add:
            try:
                images_to_add = ImageShareGroupImagesToAdd(
                    images=[
                        ImageShareGroupImageToAdd(
                            id=img["id"],
                            label=img.get("label"),
                            description=img.get("description"),
                        )
                        for img in to_add
                    ]
                )

                image_share_group.add_images(images_to_add)

                for img in to_add:
                    self.register_action(f"Added image {img['id']}")

                self.results["changed"] = True

            except Exception as e:
                self.fail(msg=f"Failed to add images: {e}")

        # Update
        for update in to_update:
            try:
                kwargs = {}
                if 'label' in update['opts']:
                    kwargs['label'] = update['opts']['label']
                if 'description' in update['opts']:
                    kwargs['description'] = update['opts']['description']

                images_to_update = ImageShareGroupImageToUpdate(
                    image_share_id=update['shared_id'],
                    **kwargs
                )

                image_share_group.update_image_share(images_to_update)
                self.register_action(f"Updated image {update['shared_id']}")
                self.results["changed"] = True
            except Exception as e:
                self.fail(msg=f"Failed to update image {update['shared_id']}: {e}")

        # Remove
        for img_shared_id in to_remove:
            try:
                image_share_group.revoke_image_share(img_shared_id)
                self.register_action(f"Removed image {img_shared_id}")
                self.results["changed"] = True
            except Exception as e:
                self.fail(msg=f"Failed to remove image {img_shared_id}: {e}")

    def _populate_results(self, sharegroup: ImageShareGroup) -> None:
        sharegroup._api_get()
        raw = sharegroup._raw_json

        images_param = self.module.params.get("images")

        if images_param is not None:
            # User explicitly provided images
            raw["images"] = images_param
        else:
            # User omitted images so fetch current images from API
            images = []
            for img in sharegroup.get_image_shares():
                shared_by = getattr(getattr(img, "image_sharing", None), "shared_by", None)
                private_id = getattr(shared_by, "source_image_id", None)
                if private_id:
                    images.append({
                        "id": private_id,
                        "label": getattr(img, "label", None),
                        "description": getattr(img, "description", None),
                    })
            raw["images"] = images

        self.results["image_share_group"] = raw

    def _handle_present(self) -> None:
        label = self.module.params.get("label")
        image_share_group = self._get_image_share_group_by_label(
            label
        )

        if not image_share_group:
            image_share_group = self._create()
            self.register_action("Created Image Share Group {0}".format(image_share_group.label))

        self._update(image_share_group)

        self._populate_results(image_share_group)

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        sharegroup = self._get_image_share_group_by_label(label)

        if sharegroup is not None:
            self.results["image_share_group"] = sharegroup._raw_json
            sharegroup.delete()
            self.register_action("Deleted image share group {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Image Share Group module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Image Share Group module"""
    Module()


if __name__ == "__main__":
    main()
