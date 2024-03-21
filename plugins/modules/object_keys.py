#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage keys."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional, Union

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.object_keys as docs
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
from linode_api4 import ObjectStorageKeys

linode_access_spec = {
    "cluster": SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The id of the cluster that the provided bucket exists under."
        ],
    ),
    "bucket_name": SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The name of the bucket to set the key's permissions for."
        ],
    ),
    "permissions": SpecField(
        type=FieldType.string,
        required=True,
        description=["The permissions to give the key."],
        choices=["read_only", "write_only", "read_write"],
    ),
}

linode_object_keys_spec = {
    "label": SpecField(
        type=FieldType.string,
        description=["The unique label to give this key."],
    ),
    "access": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_access_spec,
        description=["A list of access permissions to give the key."],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode Object Storage Keys."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_object_keys_spec,
    examples=docs.specdoc_examples,
    return_values={
        "key": SpecReturnValue(
            description="The Object Storage key in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/object-storage/#object-storage"
            "-key-view__responses",
            type=FieldType.dict,
            sample=docs.result_key_samples,
        )
    },
)


class LinodeObjectStorageKeys(LinodeModuleBase):
    """Module for creating and destroying Linode Object Storage Keys"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of = ["state", "label"]
        self.results = {
            "changed": False,
            "actions": [],
            "key": None,
        }

        self._key: Optional[ObjectStorageKeys] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_key_by_label(self, label: str) -> Optional[ObjectStorageKeys]:
        try:
            # For some reason we can't filter on label here
            keys = self.client.object_storage.keys()

            key = None
            for current_key in keys:
                if current_key.label == label:
                    key = current_key

            return key

        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get object storage key {0}: {1}".format(
                    label, exception
                )
            )

    def _create_key(
        self, label: str, bucket_access: Union[dict, List[dict]]
    ) -> Optional[ObjectStorageKeys]:
        """Creates an Object Storage key with the given label and access"""

        try:
            return self.client.object_storage.keys_create(
                label, bucket_access=bucket_access
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create object storage key: {0}".format(exception)
            )

    def _handle_key(self) -> None:
        """Updates the key defined in kwargs"""

        params = self.module.params
        label: str = params.pop("label")
        access: dict = params.get("access")

        self._key = self._get_key_by_label(label)

        if self._key is None:
            self._key = self._create_key(label, bucket_access=access)
            self.register_action("Created key {0}".format(label))

        self.results["key"] = self._key._raw_json

    def _handle_key_absent(self) -> None:
        """Deletes the key defined in kwargs"""

        label = self.module.params.pop("label")

        self._key = self._get_key_by_label(label)

        if self._key is not None:
            self.results["key"] = self._key._raw_json
            self._key.delete()
            self.register_action("Deleted key {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Constructs and calls the Linode Object Storage Key module"""

        state = kwargs.pop("state")

        if state == "absent":
            self._handle_key_absent()
            return self.results

        self._handle_key()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Object Storage key module"""

    LinodeObjectStorageKeys()


if __name__ == "__main__":
    main()
