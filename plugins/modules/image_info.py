#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode image."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import Image

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    filter_null_values
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_info as docs

spec = dict(
    # Disable the default values
    state=dict(type='str', required=False, doc_hide=True),

    id=dict(type='str', description='The ID of the image.'),
    label=dict(type='str', description='The label of the image.'),
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode Image.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        image=dict(
            description='The image in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/images/#image-view__responses',
            type='dict',
            sample=docs_parent.result_image_samples
        )
    )
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.module_arg_spec = spec
        self.results = {
            'image': None
        }

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=[('id', 'label')],
                         mutually_exclusive=[('id', 'label')])

    def _get_image_by_label(self, label: str) -> Optional[Image]:
        try:
            return self.client.images(Image.label == label)[0]
        except IndexError:
            return self.fail(msg='failed to get image with label {0}: '
                                 'image does not exist'.format(label))
        except Exception as exception:
            return self.fail(msg='failed to get image {0}: {1}'.format(label, exception))

    def _get_image_by_id(self, image_id: int) -> Image:
        return self._get_resource_by_id(Image, image_id)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for user info module"""

        params = filter_null_values(self.module.params)

        if 'id' in params:
            self.results['image'] = self._get_image_by_id(params.get('id'))._raw_json

        if 'label' in params:
            self.results['image'] = self._get_image_by_label(params.get('label'))._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == '__main__':
    main()
