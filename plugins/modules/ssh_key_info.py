#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode SSH key."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import SSHKey

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    filter_null_values
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

# import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.stackscript \
#     as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ssh_key_info \
    as docs

linode_ssh_key_info_spec = dict(
    id=dict(type='int', description='The ID of the SSH key.'),
    label=dict(type='str', description='The label of the SSH key.'),
)

specdoc_meta = dict(
    description=[
        'Get info about the Linode SSH public key.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_ssh_key_info_spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        ssh_key=dict(
            description='The SSH key in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/profile/'
                     '#ssh-key-view__response-samples',
            type='dict',
            # sample=docs_parent.result_stackscript_samples
        )
    )
)


class LinodeSSHKeyInfo(LinodeModuleBase):
    """Module for getting Linode SSH public key"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_ssh_key_info_spec
        self.results = {
            'ssh_key': None
        }

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=[('id', 'label')],
                         mutually_exclusive=[('id', 'label')])

    def _get_ssh_key_by_label(self, label: str) -> Optional[SSHKey]:
        try:
            ssh_keys = self.client.profile.ssh_keys(SSHKey.label == label)
            if not ssh_keys:
                return self.fail(msg=f'failed to get ssh key with label {label}: '
                                    'ssh key does not exist')
            return ssh_keys[0]  # maybe return whole list?
        except Exception as exception:
            return self.fail(msg=f'failed to get ssh key {label}: {exception}')

    def _get_ssh_key_by_id(self, ssh_key_id: int) -> Optional[SSHKey]:
        try:
            ssh_key = SSHKey(self.client, ssh_key_id)
            ssh_key._api_get()
            return ssh_key
        except Exception as exception:
            return self.fail(msg=f'failed to get ssh key with id {ssh_key_id}: {exception}')

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ssh_key_info module"""

        params = filter_null_values(self.module.params)

        if 'id' in params:
            ssh_key = self._get_ssh_key_by_id(params.get('id'))
        elif 'label' in params:
            ssh_key = self._get_ssh_key_by_label(params.get('label'))

        self.results['ssh_key'] = ssh_key._raw_json
        return self.results


def main() -> None:
    """Constructs and calls the module"""
    LinodeSSHKeyInfo()


if __name__ == '__main__':
    main()
