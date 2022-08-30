#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode user."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import User

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user_info as docs

spec = dict(
    # Disable the default values
    label=dict(type='str', required=False, doc_hide=True),
    state=dict(type='str', required=False, doc_hide=True),

    username=dict(type='str', required=True,
                  description='The username of the user.')
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode User.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        user=dict(
            description='The user info in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/account/#user-view',
            type='dict',
            sample=docs.result_user_samples
        ),
        grants=dict(
            description='The grants info in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/account/#users-grants-view__response-samples',
            type='dict',
            sample=docs.result_grants_samples
        )
    )
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.required_one_of: List[str] = []
        self.results = dict(
            user=None,
        )

        self.module_arg_spec = spec

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for user info module"""

        user = self.client.account.users(User.username == self.module.params.get('username'))
        grants = user.grants

        self.results['user'] = user._raw_json
        self.results['grants'] = grants._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == '__main__':
    main()
