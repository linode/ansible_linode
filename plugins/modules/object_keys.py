#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage keys."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.object_keys as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ObjectStorageKeys

linode_access_spec = {
    "region": SpecField(
        type=FieldType.string,
        description=[
            "The region of the cluster that the provided bucket exists under."
        ],
        conflicts_with=["cluster"],
    ),
    "cluster": SpecField(
        type=FieldType.string,
        description=[
            "The id of the cluster that the provided bucket exists under.",
            "**NOTE: This field has been deprecated because it "
            + "relies on deprecated API endpoints. Going forward, `region` will "
            + "be the preferred way to designate where Object Storage resources "
            + "should be created.**",
        ],
        conflicts_with=["region"],
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
    "regions": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=["A list of regions to scope this key to."],
        editable=True,
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
        self,
        label: str,
        bucket_access: Optional[List[Dict[str, Any]]],
        regions: Optional[List[str]],
    ) -> Optional[ObjectStorageKeys]:
        """Creates an Object Storage key with the given label and access"""

        # The API will reject explicit null values for `bucket_access.region`
        if bucket_access is not None:
            bucket_access = [
                filter_null_values(grant) for grant in bucket_access
            ]

        try:
            return self.client.object_storage.keys_create(
                label, bucket_access=bucket_access, regions=regions
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create object storage key: {0}".format(exception)
            )

    @staticmethod
    def _access_changed(key: ObjectStorageKeys, params: Dict[str, Any]) -> bool:
        """
        Returns whether the user has made any effective changes to the `access` field.

        NOTE: This requires special logic to maintain backwards compatibility
        with the `cluster` field.
        """

        configured_access = params.get("access")
        if configured_access is None:
            return False

        # Map the region and bucket name to a grant
        access = {
            (grant.region, grant.bucket_name): grant
            for grant in key.bucket_access
        }

        for configured_grant in configured_access:
            configured_region = configured_grant.get("region")
            configured_permissions = configured_grant.get("permissions")

            # Hack to extract the region from a configured cluster
            if configured_region is None:
                configured_region = configured_grant.get("cluster").split("-1")[
                    0
                ]

            grant_key = (configured_region, configured_grant.get("bucket_name"))

            grant = access.get(grant_key)
            if grant is None or configured_permissions != grant.permissions:
                return True

            del access[grant_key]

        # If true, the user attempted to remove a grant
        return len(access) > 0

    def _validate_updates(
        self, key: ObjectStorageKeys, params: Dict[str, Any]
    ) -> None:
        """
        Raises an error if any invalid update operations are attempted.
        """

        if self._access_changed(key, params):
            self.fail("`access` is not an updatable field")

    def _attempt_update_key(
        self, key: ObjectStorageKeys, params: Dict[str, Any]
    ) -> None:
        """
        Attempts to update the given OBJ key.
        """

        self._validate_updates(key, params)

        put_body = {}

        # We can't use handle_updates here because the structure under `regions`
        # differs between the request and response
        configured_regions = params.get("regions") or []
        flattened_regions = set(v.id for v in key.regions)

        # Regions from bucket_access will implicitly be added to the
        # `regions` attribute, so we should account for that here
        for grant in key.bucket_access or []:
            configured_regions.append(grant.region)

        if (
            configured_regions is not None
            and set(configured_regions) != flattened_regions
        ):
            put_body["regions"] = configured_regions
            self.register_action(
                f"Updated regions from {list(flattened_regions)} to {configured_regions}"
            )

        # Apply changes
        if len(put_body) > 0:
            self._client.put(
                ObjectStorageKeys.api_endpoint, model=key, data=put_body
            )

            # Refresh the key object
            self._key._api_get()

    def _handle_key(self) -> None:
        """Updates the key defined in kwargs"""

        params = self.module.params
        label: str = params.get("label")
        access: List[Dict[str, Any]] = params.get("access")
        regions: List[str] = params.get("regions")

        self._key = self._get_key_by_label(label)

        if self._key is None:
            self._key = self._create_key(
                label, bucket_access=access, regions=regions
            )
            self.register_action("Created key {0}".format(label))

            # NOTE: If the key is refreshed at all after creation,
            # make sure you preserve the secret_key :)
        else:
            self._attempt_update_key(self._key, params)

        self.results["key"] = self._key._raw_json

    def _handle_key_absent(self) -> None:
        """Deletes the key defined in kwargs"""

        label = self.module.params.pop("label")

        self._key = self._get_key_by_label(label)

        if self._key is not None:
            self.results["key"] = self._key._raw_json
            self._key.delete()
            self.register_action("Deleted key {0}".format(label))

    def _attempt_warnings(self, **kwargs: Any) -> None:
        """
        Raises warnings depending on the user-defined module arguments.
        """

        # Logic to warn if the `cluster` field has been specified
        access: Optional[List] = kwargs.get("access", None)

        # If cluster has been defined for any of the `access` objects,
        # raise a deprecation warning
        if access is not None and any(
            v is not None for v in access if v.get("cluster", None)
        ):
            self.warn(
                "The access.cluster field has been deprecated because it relies "
                "on deprecated API endpoints.\n"
                "Going forward, region will be the preferred way to designate where Object "
                "Storage resources should be created."
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Constructs and calls the Linode Object Storage Key module"""

        self._attempt_warnings(**kwargs)

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
