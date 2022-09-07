#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Images."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
from typing import Optional, cast, Any, Set

import polling
from linode_api4 import Image

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
        description='This Image\'s unique label.'),
    state=dict(
        type='str',
        choices=['present', 'absent'],
        required=True,
        description='The state of this StackScript.',
    ),

    disk_id=dict(
        type='int',
        description='Images that can be deployed using this StackScript.',
    ),
    description=dict(
        type='str',
        description='A description for the Image.',
    ),

    wait=dict(
        type='bool', default=True,
        description='Wait for the image to have status `available` before returning.'),

    wait_timeout=dict(
        type='int', default=240,
        description='The amount of time, in seconds, to wait for an image to '
                    'have status `available`.'
    )
)

specdoc_meta = dict(
    description=[
        'Manage a Linode Image.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=SPEC,
    examples=docs.specdoc_examples,
    return_values=dict(
        stackscript=dict(
            description='The Image in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/images/'
                     '#image-view__response-samples',
            type='dict',
            sample=docs.result_stackscript_samples
        )
    )
)

MUTABLE_FIELDS = {
    'description'
}


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Images"""

    def __init__(self) -> None:
        self.module_arg_spec = SPEC
        self.required_one_of = ['state', 'label']
        self.results = dict(
            changed=False,
            actions=[],
            image=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of,
                         required_if=[('state', 'present', ['disk_id'])])

    def _get_image_by_label(self, label: str) -> Optional[Image]:
        try:
            return self.client.images(Image.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get image {0}: {1}'.format(label, exception))

    def _wait_for_image_status(self, image: Image, status: Set[str]) -> None:
        def poll_func() -> bool:
            image._api_get()
            return image.status in status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=10,
                timeout=self.module.params.get('wait_timeout'),
            )
        except polling.TimeoutException:
            self.fail('failed to wait for image status: timeout period expired')

    def _create_image_from_disk(self) -> Optional[Image]:
        disk_id = self.module.params.get('disk_id')
        label = self.module.params.get('label')
        description = self.module.params.get('description')

        try:
            return self.client.image_create(disk_id, label=label, description=description)
        except Exception as exception:
            return self.fail(msg='failed to create image: {0}'.format(exception))

    def _create_image(self) -> Optional[Image]:
        if self.module.params.get('disk_id') is not None:
            image = self._create_image_from_disk()

            if self.module.params.get('wait'):
                self._wait_for_image_status(image, {'available'})

            return image

        self.fail(msg='no handler found for image')

    # def _update_stackscript(self, stackscript: Image) -> None:
    #     stackscript._api_get()
    #
    #     params = filter_null_values(self.module.params)
    #
    #     handle_updates(stackscript, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get('label')

        image = self._get_image_by_label(label)

        # Create the image if it does not already exist
        if image is None:
            image = self._create_image()
            self.register_action('Created image {0}'.format(label))

        # self._update_stackscript(image)

        # Force lazy-loading
        image._api_get()

        self.results['image'] = image._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get('label')

        image = self._get_image_by_label(label)

        if image is not None:
            self.results['image'] = image._raw_json
            image.delete()
            self.register_action('Deleted image {0}'.format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Image module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Image module"""
    Module()


if __name__ == '__main__':
    main()
