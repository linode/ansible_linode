#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Users."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
from typing import Optional, cast, Any, Set

import polling
from linode_api4 import User

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user as docs

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    handle_updates, filter_null_values

SPEC = dict(
    # We don't use label for this module
    label=dict(
        type='str',
        required=False,
        doc_hide=True),

    username=dict(
        type='str',
        required=True,
        description='The username of this user.',
    ),
    state=dict(
        type='str',
        choices=['present', 'absent'],
        required=True,
        description='The state of this user.',
    ),

    restricted=dict(
        type='bool',
        description='If true, the User must be granted access to perform actions or access entities on this Account.',
        default=True,
    ),
    email=dict(
        type='str',
        description=['The email address for the User.',
                     'Linode sends emails to this address for account management communications.',
                     'May be used for other communications as configured.']
    )
)

specdoc_meta = dict(
    description=[
        'Manage a Linode User.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=SPEC,
    examples=docs.specdoc_examples,
    return_values=dict(
        user=dict(
            description='The user in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/account/'
                     '#user-view__response-samples',
            type='dict',
            sample=docs.result_user_samples
        )
    )
)

MUTABLE_FIELDS = {
    'email',
    'restricted'
}


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Users"""

    def __init__(self) -> None:
        self.module_arg_spec = SPEC
        self.required_one_of = ['state', 'username']
        self.results = dict(
            changed=False,
            actions=[],
            user=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of,
                         required_if=[('state', 'present', ['email'])])

    def _get_user_by_username(self, username: str) -> Optional[User]:
        try:
            return self.client.account.users(User.username == username)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get user {0}: {1}'.format(username, exception))

    def _create_user(self) -> Optional[User]:
        params = filter_null_values(self.module.params)
        username = params.pop('username')
        email = params.pop('email')

        for key in {'api_token', 'api_version', 'state'}:
            params.pop(key)

        try:
            return self.client.account.user_create(email, username, **params)
        except Exception as exception:
            return self.fail(msg='failed to create user: {0}'.format(exception))

    def update_user(self, user: User) -> None:
        user._api_get()

        params = self.module.params

        handle_updates(user, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params
        username = params.get('username')

        user = self._get_user_by_username(username)

        # Create the user if it does not already exist
        if user is None:
            user = self._create_user()
            self.register_action('Created user {0}'.format(username))

        self.update_user(user)

        # Force lazy-loading
        user._api_get()

        self.results['user'] = user._raw_json

    def _handle_absent(self) -> None:
        username: str = self.module.params.get('username')

        user = self._get_user_by_username(username)

        if user is not None:
            self.results['user'] = user._raw_json
            user.delete()
            self.register_action('Deleted user {0}'.format(user))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode user module"""
    Module()


if __name__ == '__main__':
    main()
