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

SPEC_GRANTS_GLOBAL = {
    'account_access': {
        'type:': 'str',
        'choices': ['read_only', 'read_write'],
        'description': [
            'The level of access this User has to Account-level actions, like billing information.',
            'A restricted User will never be able to manage users.'],
        'default': 'read_only',
    },
    'add_databases': {
        'type': 'bool',
        'description': 'If true, this User may add Managed Databases.',
        'default': False,
    },
    'add_domains': {
        'type': 'bool',
        'description': 'If true, this User may add Domains.',
        'default': False,
    },
    'add_firewalls': {
        'type': 'bool',
        'description': 'If true, this User may add firewalls.',
        'default': False,
    },
    'add_images': {
        'type': 'bool',
        'description': 'If true, this User may add images.',
        'default': False,
    },
    'add_linodes': {
        'type': 'bool',
        'description': 'If true, this User may add Linodes.',
        'default': False,
    },
    'add_longview': {
        'type': 'bool',
        'description': 'If true, this User may add LongView.',
        'default': False,
    },
    'add_nodebalancers': {
        'type': 'bool',
        'description': 'If true, this User may add NodeBalancers.',
        'default': False,
    },
    'add_stackscripts': {
        'type': 'bool',
        'description': 'If true, this User may add StackScripts.',
        'default': False,
    },
    'add_volumes': {
        'type': 'bool',
        'description': 'If true, this User may add volumes.',
        'default': False,
    },
    'cancel_account': {
        'type': 'bool',
        'description': 'If true, this User may add cancel the entire account.',
        'default': False,
    },
    'longview_subscription': {
        'type': 'bool',
        'description': 'If true, this User may manage the Account’s Longview subscription.',
        'default': False,
    },
}

SPEC_GRANTS_RESOURCE = {
    'type': {
        'type:': 'str',
        'choices': ['domain', 'image', 'linode', 'longview', 'nodebalancer', 'stackscript', 'volume'],
        'description': [
            'The type of resource to grant access to.'],
        'required': True,
    },
    'id': {
        'type': 'int',
        'description': 'The ID of the resource to grant access to.',
        'required': True,
    },
    'permissions': {
        'type': 'str',
        'choices': ['read_only', 'read_write'],
        'description': 'The level of access this User has to this entity. If null, this User has no access.',
    },
}

SPEC_GRANTS = {
    'global': {
        'type': 'dict',
        'description': 'A structure containing the Account-level grants a User has.',
        'options': SPEC_GRANTS_GLOBAL,
    },
    'resource': {
        'description': 'A list of resource grants to give to the user.',
        'type': 'list',
        'elements': 'dict',
        'options': SPEC_GRANTS_RESOURCE
    }
}

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
    ),
    grants=dict(
        type='dict',
        description='Update the grants a User has.',
        options=SPEC_GRANTS
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
        ),
        grants=dict(
            description='The grants info in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/account/#users-grants-view__response-samples',
            type='dict',
            sample=docs.result_grants_samples
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
