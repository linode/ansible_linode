#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list SSH keys in their Linode profile."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ssh_key_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    construct_api_filter,
    get_all_paginated,
)

spec_filter = dict(
    name=dict(
        type="str",
        required=True,
        description=[
            "The name of the field to filter on.",
            (
                "Valid filterable attributes can be found here: "
                "https://www.linode.com/docs/api/profile/"
                "#ssh-keys-list"
            ),
        ],
    ),
    values=dict(
        type="list",
        elements="str",
        required=True,
        description=[
            "A list of values to allow for this field.",
            "Fields will pass this filter if at least one of these values matches.",
        ],
    ),
)

spec = dict(
    # Disable the default values
    state=dict(type="str", required=False, doc_hide=True),
    label=dict(type="str", required=False, doc_hide=True),
    order=dict(
        type="str",
        description="The order to list ssh keys in.",
        default="asc",
        choices=["desc", "asc"],
    ),
    order_by=dict(type="str", description="The attribute to order ssh keys by."),
    filters=dict(
        type="list",
        elements="dict",
        options=spec_filter,
        description="A list of filters to apply to the resulting ssh keys.",
    ),
    count=dict(
        type="int",
        description=[
            "The number of results to return.",
            "If undefined, all results will be returned.",
        ],
    ),
)

specdoc_meta = dict(
    description=["List and filter on SSH keys in the Linode profile."],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.ssh_key_list_specdoc_examples,
    return_values=dict(
        ssh_keys=dict(
            description="The returned SSH keys.",
            docs_url=("https://www.linode.com/docs/api/profile/" "#ssh-keys-list"),
            type="list",
            elements="dict",
            sample=docs.result_ssh_key_list_samples,
        )
    ),
)


class SSHKeyListModule(LinodeModuleBase):
    """Module for getting a list of SSH keys in the Linode profile"""

    def __init__(self) -> None:
        self.module_arg_spec = spec
        self.results: Dict[str, Any] = {"ssh_keys": []}

        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for SSH key list module"""

        filter_dict = construct_api_filter(self.module.params)

        self.results["ssh_keys"] = get_all_paginated(
            self.client,
            "/profile/sshkeys",
            filter_dict,
            num_results=self.module.params["count"],
        )
        return self.results


def main() -> None:
    """Constructs and calls the module"""
    SSHKeyListModule()


if __name__ == "__main__":
    main()
