#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode resource locks."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lock as docs
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
from linode_api4 import Lock

SPEC = {
    "id": SpecField(
        type=FieldType.integer,
        description=[
            "The ID of the lock to delete.",
            "Only used when state is absent; ignored when state is present.",
        ],
    ),
    "entity_type": SpecField(
        type=FieldType.string,
        choices=[
            "linode",
            "volume",
            "nodebalancer",
            "lkecluster",
            "lkenodepool",
        ],
        description=[
            "The type of entity to lock.",
            "Supported entity types: 'linode', 'volume', 'nodebalancer', 'lkecluster', 'lkenodepool'.",
        ],
    ),
    "entity_id": SpecField(
        type=FieldType.integer,
        description=["The ID of the entity to lock."],
    ),
    "lock_type": SpecField(
        type=FieldType.string,
        choices=["cannot_delete", "cannot_delete_with_subresources"],
        description=[
            "The type of lock to apply.",
            "Only one delete-protection lock may exist per resource at a time.",
            "'cannot_delete' - Prevents deletion of the entity.",
            "'cannot_delete_with_subresources' - Prevents deletion of the ",
            "entity and its subresources (disks, configs, etc.).",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of the lock."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Create and delete Linode resource locks.",
        "Resource locks protect resources from accidental deletion.",
        "Locks can only be created and deleted by unrestricted users.",
        "NOTE: Locks cannot be updated. To change a lock, delete it and create a new one.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "lock": SpecReturnValue(
            description="The lock in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-lock",
            type=FieldType.dict,
            sample=docs.result_lock_samples,
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
    """Module for creating and destroying Linode resource locks"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"changed": False, "actions": [], "lock": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_if=[
                ("state", "present", ["entity_type", "entity_id", "lock_type"]),
                ("state", "absent", ["id"]),
            ],
        )

    def _create_lock(self) -> Lock | None:
        """Create a new resource lock."""
        params = filter_null_values(
            {
                "entity_type": self.module.params.get("entity_type"),
                "entity_id": self.module.params.get("entity_id"),
                "lock_type": self.module.params.get("lock_type"),
            }
        )

        try:
            result = self.client.locks.create(**params)
            return result
        except Exception as exception:
            self.fail(msg=f"Failed to create lock: {exception}")

    def _delete_lock(self, lock: Lock) -> None:
        """Delete a resource lock."""
        try:
            lock.delete()
        except Exception as exception:
            self.fail(msg=f"Failed to delete lock: {exception}")

    def _find_existing_lock(self) -> Optional[dict]:
        """Find an existing lock for the given entity."""
        entity_type = self.module.params.get("entity_type")
        entity_id = self.module.params.get("entity_id")
        lock_type = self.module.params.get("lock_type")

        try:
            locks = self.client.locks()
            for lock in locks:
                if (
                    lock.entity.type == entity_type
                    and lock.entity.id == entity_id
                    and lock.lock_type == lock_type
                ):
                    return lock._raw_json
            return None
        except Exception as exception:
            self.fail(msg=f"Failed to list locks: {exception}")

    def _handle_present(self) -> None:
        """Handle state=present - create a lock if it doesn't exist."""
        # Check if lock already exists
        existing_lock = self._find_existing_lock()

        if existing_lock is not None:
            # Lock already exists, no changes needed
            self.results["lock"] = existing_lock
            return

        # Create the lock
        lock = self._create_lock()
        if not lock:
            return

        self.register_action(
            f"Created lock {lock.id} on "
            f"{lock.entity.type} "
            f"{lock.entity.id}"
        )
        self.results["lock"] = lock._raw_json

    def _handle_absent(self) -> None:
        """Handle state=absent - delete the lock."""
        lock_id = self.module.params.get("id")

        try:
            lock = self.client.load(Lock, lock_id)
            lock._api_get()
        except Exception:
            # Lock doesn't exist, nothing to do
            return

        self.results["lock"] = lock._raw_json
        self._delete_lock(lock)
        self.register_action(f"Deleted lock {lock_id}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for lock module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
        else:
            self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Lock module"""
    Module()


if __name__ == "__main__":
    main()
