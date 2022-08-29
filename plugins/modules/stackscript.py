#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode StackScripts."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
from typing import Optional, cast, Any, Set

import polling
from linode_api4 import StackScript

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    handle_updates, filter_null_values

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.stackscript as docs

SPEC = dict(
    label=dict(
        type='str',
        required=True,
        description='This StackScript\'s unique label.'),
    state=dict(
        type='str',
        choices=['present', 'absent'],
        required=True,
        description='The state of this StackScript.',
    ),

    description=dict(
        type='str',
        description='A description for the StackScript.',
    ),
    images=dict(
        type='list',
        elements='str',
        description='Images that can be deployed using this StackScript.',
    ),
    is_public=dict(
        type='bool',
        description='This determines whether other users can use your StackScript.',
    ),
    rev_note=dict(
        type='str',
        description='This field allows you to add notes for '
                    'the set of revisions made to this StackScript.',
    ),
    script=dict(
        type='str',
        description='The script to execute when provisioning a new Linode with this StackScript.'
    )
)

specdoc_meta = dict(
    description=[
        'Manage a Linode StackScript.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=SPEC,
    examples=docs.specdoc_examples,
    return_values=dict(
        stackscript=dict(
            description='The StackScript in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/stackscripts/'
                     '#stackscript-create__response-samples',
            type='dict',
            sample=docs.result_stackscript_samples
        )
    )
)

MUTABLE_FIELDS = {
    'description',
    'images',
    'is_public',
    'rev_note',
    'script'
}


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode StackScripts"""

    def __init__(self) -> None:
        self.module_arg_spec = SPEC
        self.required_one_of = ['state', 'label']
        self.results = dict(
            changed=False,
            actions=[],
            stackscript=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of,
                         required_if=[('state', 'present', ('images', 'script'))])

    def _get_stackscript_by_label(self, label: str) -> Optional[StackScript]:
        try:
            return self.client.linode.stackscripts(StackScript.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get stackscript {0}: {1}'.format(label, exception))

    def _create_stackscript(self) -> Optional[StackScript]:
        params = copy.deepcopy(self.module.params)
        label = params.pop('label')
        script = params.pop('script')
        images = params.pop('images')

        try:
            return self.client.linode.stackscript_create(label, script, images, **params)
        except Exception as exception:
            return self.fail(msg='failed to create stackscript: {0}'.format(exception))

    def _update_stackscript(self, stackscript: StackScript) -> None:
        stackscript._api_get()

        params = filter_null_values(self.module.params)

        handle_updates(stackscript, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get('label')

        stackscript = self._get_stackscript_by_label(label)

        # Create the stackscript if it does not already exist
        if stackscript is None:
            stackscript = self._create_stackscript()
            self.register_action('Created stackscript {0}'.format(label))

        self._update_stackscript(stackscript)

        # Force lazy-loading
        stackscript._api_get()

        self.results['stackscript'] = stackscript._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get('label')

        stackscript = self._get_stackscript_by_label(label)

        if stackscript is not None:
            self.results['stackscript'] = stackscript._raw_json
            stackscript.delete()
            self.register_action('Deleted stackscript {0}'.format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for StackScript module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the StackScript module"""
    Module()


if __name__ == '__main__':
    main()
