#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Token."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import PersonalAccessToken

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    filter_null_values
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token_info as docs

spec = dict(
    # Disable the default values
    state=dict(type='str', required=False, doc_hide=True),

    id=dict(type='int', description='The ID of the token.'),
    label=dict(type='str', description='The label of the token.'),
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode Personal Access Token.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        token=dict(
            description='The token in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/profile/'
                     '#personal-access-token-create__response-samples',
            type='dict',
            sample=docs_parent.result_token_samples
        )
    )
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode token"""

    def __init__(self) -> None:
        self.module_arg_spec = spec
        self.results = {
            'token': None
        }

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=[('id', 'label')],
                         mutually_exclusive=[('id', 'label')],
                         resource_name = "personal token")

    def _get_token_by_label(self, label: str) -> Optional[PersonalAccessToken]:
        try:
            return self.client.profile.tokens(PersonalAccessToken.label == label)[0]
        except IndexError:
            return self.fail(msg='failed to get token with label {0}: '
                                 'token does not exist'.format(label))
        except Exception as exception:
            return self.fail(msg='failed to get token {0}: {1}'.format(label, exception))

    def _get_token_by_id(self, token_id: int) -> PersonalAccessToken:
        return self._get_resource_by_id(PersonalAccessToken, token_id)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token info module"""

        params = filter_null_values(self.module.params)

        if 'id' in params:
            self.results['token'] = self._get_token_by_id(params.get('id'))._raw_json

        if 'label' in params:
            self.results['token'] = self._get_token_by_label(params.get('label'))._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == '__main__':
    main()
