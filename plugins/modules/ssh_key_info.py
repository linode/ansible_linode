#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode SSH key."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ssh_key_info as docs
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
from linode_api4 import SSHKey

linode_ssh_key_info_spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.integer,
        conflicts_with=["label"],
        description=["The ID of the SSH key."],
    ),
    "label": SpecField(
        type=FieldType.string,
        conflicts_with=["id"],
        description=["The label of the SSH key."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about the Linode SSH public key."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_ssh_key_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "ssh_key": SpecReturnValue(
            description="The SSH key in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/profile/"
            "#ssh-key-view__response-samples",
            type=FieldType.dict,
            sample=docs.ssh_key_info_response_sample,
        )
    },
)


class LinodeSSHKeyInfo(LinodeModuleBase):
    """Module for getting Linode SSH public key"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"ssh_key": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
            mutually_exclusive=[("id", "label")],
        )

    def _get_ssh_key_by_label(self, label: str) -> Optional[SSHKey]:
        try:
            ssh_keys = self.client.profile.ssh_keys(SSHKey.label == label)
            if not ssh_keys:
                return self.fail(
                    msg=f"failed to get ssh key with label {label}: "
                    "ssh key does not exist"
                )
            return ssh_keys[0]  # maybe return whole list?
        except Exception as exception:
            return self.fail(msg=f"failed to get ssh key {label}: {exception}")

    def _get_ssh_key_by_id(self, ssh_key_id: int) -> Optional[SSHKey]:
        return self._get_resource_by_id(SSHKey, ssh_key_id)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ssh_key_info module"""

        params = filter_null_values(self.module.params)

        if "id" in params:
            ssh_key = self._get_ssh_key_by_id(params.get("id"))
        elif "label" in params:
            ssh_key = self._get_ssh_key_by_label(params.get("label"))

        self.results["ssh_key"] = ssh_key._raw_json
        return self.results


def main() -> None:
    """Constructs and calls the module"""
    LinodeSSHKeyInfo()


if __name__ == "__main__":
    main()
