#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Users."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
from typing import Optional, cast, Any, Set, Dict

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
            'The level of access this User has to Account-level actions, '
            'like billing information.',
            'A restricted User will never be able to manage users.'],
        'default': None
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
        'description': 'If true, this User may manage the Account’s '
                       'Longview subscription.',
        'default': False,
    },
}

SPEC_GRANTS_RESOURCE = {
    'type': {
        'type:': 'str',
        'choices': ['domain', 'image', 'linode', 'longview',
                    'nodebalancer', 'stackscript', 'volume'],
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
        'description': 'The level of access this User has to this entity. '
                       'If null, this User has no access.',
        'required': True
    },
}

SPEC_GRANTS = {
    'global': {
        'type': 'dict',
        'description': 'A structure containing the Account-level grants a User has.',
        'options': SPEC_GRANTS_GLOBAL,
    },
    'resources': {
        'description': 'A list of resource grants to give to the user.',
        'type': 'list',
        'elements': 'dict',
        'options': SPEC_GRANTS_RESOURCE
    }
}

SPEC = {
    # We don't use label for this module
    'label': {
        'type': 'str',
        'required': False,
        'doc_hide': True
    },
    'username': {
        'type': 'str',
        'required': True,
        'description': 'The username of this user.',
    },
    'state': {
        'type': 'str',
        'choices': ['present', 'absent'],
        'required': True,
        'description': 'The state of this user.',
    },
    'restricted': {
        'type': 'bool',
        'description': 'If true, the User must be granted access to perform '
                       'actions or access entities on this Account.',
        'default': True,
    },
    'email': {
        'type': 'str',
        'description': ['The email address for the User.',
                        'Linode sends emails to this address for account '
                        'management communications.',
                        'May be used for other communications as configured.']
    },
    'grants': {
        'type': 'dict',
        'description': 'Update the grants a User has.',
        'options': SPEC_GRANTS
    }
}

specdoc_meta = {
    'description': [
        'Manage a Linode User.'
    ],
    'requirements': global_requirements,
    'author': global_authors,
    'spec': SPEC,
    'examples': docs.specdoc_examples,
    'return_values': {
        'user': {
            'description': 'The user in JSON serialized form.',
            'docs_url': 'https://www.linode.com/docs/api/account/'
                        '#user-view__response-samples',
            'type': 'dict',
            'sample': docs.result_user_samples
        },
        'grants': {
            'description': 'The grants info in JSON serialized form.',
            'docs_url': 'https://www.linode.com/docs/api/account/'
                        '#users-grants-view__response-samples',
            'type': 'dict',
            'sample': docs.result_grants_samples
        }
    }
}

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
            grants=None
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of,
                         required_if=[('state', 'present', ['email'])])

    @staticmethod
    def _normalize_grants_params(grants: Dict[str, any]) -> Dict[str, any]:
        result = {}

        if 'global' in grants:
            result['global'] = grants['global']

        if 'resources' not in grants or grants['resources'] is None:
            return result

        for resource_grant in grants['resources']:
            entity_type = resource_grant.get('type').lower()
            entity_id = resource_grant.get('id')
            permissions = resource_grant.get('permissions')

            if entity_type not in result:
                result[entity_type] = []

            result[entity_type].append({
                'id': entity_id,
                'permissions': permissions
            })

        return result

    def _get_raw_grants(self, user: User) -> Optional[Dict[any, str]]:
        try:
            return self.client.get('/account/users/{0}/grants'.format(user.id))
        except Exception as exception:
            return self.fail(msg='failed to get user grants: {0}'.format(exception))

    @staticmethod
    def _compare_grants(old_grants: Dict[str, any], new_grants: Dict[str, any]) -> bool:
        normalized_grants = {'global': old_grants['global']}

        # Remove all implicitly created values to allow for proper diffing
        for key, resource in old_grants.items():
            if not isinstance(resource, list):
                continue

            result_list = [
                resource_grant for resource_grant in resource
                if resource_grant['permissions'] is not None
            ]

            if len(result_list) > 0:
                normalized_grants[key] = result_list

        return new_grants == normalized_grants

    @staticmethod
    def _merge_grants(old_grants: Dict[str, any], param_grants: Dict[str, any]) -> Dict[any, str]:
        # This function is necessary as we want users to explicitly specify all grants that
        # should be given to a user.

        result = {'global': {}}

        # Set the global grant values from the params
        if param_grants['global']:
            result['global'] = param_grants['global']

        # Create a dict as a reference for later
        new_grant_map = {}
        for key, resource in param_grants.items():
            if not isinstance(resource, list):
                continue

            for grant in resource:
                if key not in new_grant_map:
                    new_grant_map[key] = {}

                new_grant_map[key][grant['id']] = grant

        # Merge the output
        for key, resource in old_grants.items():
            if not isinstance(resource, list):
                continue

            if key not in result:
                result[key] = []

            for grant in resource:
                # Use the existing grant
                if key in new_grant_map and grant['id'] in new_grant_map[key]:
                    result[key].append(new_grant_map[key][grant['id']])
                    continue

                # Remove permissions for all other grants
                result[key].append({
                    'id': grant['id'],
                    'permissions': None
                })

        return result

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

        for key in {'api_token', 'api_version', 'state', 'grants'}:
            params.pop(key)

        try:
            return self.client.account.user_create(email, username, **params)
        except Exception as exception:
            return self.fail(msg='failed to create user: {0}'.format(exception))

    def _update_grants(self, user: User) -> None:
        params = self.module.params

        if 'grants' not in params or params['grants'] is None or not params['restricted']:
            return

        param_grants = self._normalize_grants_params(params['grants'])
        raw_grants = self._get_raw_grants(user)

        if self._compare_grants(raw_grants, param_grants):
            return

        # We need to merge the old grants with the new grants to properly
        # give/revoke grants declaratively
        put_body = self._merge_grants(raw_grants, param_grants)

        self.client.put('/account/users/{0}/grants'.format(user.id), data=put_body)
        self.register_action('Updated grants')

    def _update_user(self, user: User) -> None:
        user._api_get()

        params = filter_null_values(self.module.params)

        if 'grants' in params:
            params.pop('grants')

        handle_updates(user, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params
        username = params.get('username')

        user = self._get_user_by_username(username)

        # Create the user if it does not already exist
        if user is None:
            user = self._create_user()
            self.register_action('Created user {0}'.format(username))

        self._update_user(user)

        self._update_grants(user)

        # Force lazy-loading
        user._api_get()

        self.results['user'] = user._raw_json
        self.results['grants'] = self._get_raw_grants(user)

    def _handle_absent(self) -> None:
        username: str = self.module.params.get('username')

        user = self._get_user_by_username(username)

        if user is not None:
            self.results['user'] = user._raw_json
            self.results['grants'] = self._get_raw_grants(user)
            user.delete()
            self.register_action('Deleted user {0}'.format(user.username))

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
