#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode IPv6 range."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import IPv6Range

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import filter_null_values
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ipv6_range_info as docs

spec = dict(
    # Disable the default values
    state=dict(type='str', required=False, doc_hide=True),
    label=dict(type='str', required=False, doc_hide=True),

    range=dict(type='str', description='The IPv6 range to access.'),
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode IPv6 range.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        range=dict(
            description='The IPv6 range in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/networking/'
                     '#ipv6-range-view__response-samples',
            type='dict',
            sample=docs.result_range_samples
        )
    )
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode IPv6 range"""

    def __init__(self) -> None:
        self.module_arg_spec = spec
        self.results = {
            'range': None
        }

        super().__init__(module_arg_spec=self.module_arg_spec)

    def _get_range(self, address: str) -> IPv6Range:
        try:
            # Workaround for endpoint formatting issue
            data = self.client.get(IPv6Range.api_endpoint.format(address))

            result = IPv6Range(self.client, address, json=data)
            return result
        except Exception as exception:
            self.fail(msg='failed to get range with address {0}: {1}'
                      .format(address, exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ipv6_range_info module"""

        params = filter_null_values(self.module.params)

        # We want to omit the prefix length if specified
        address = params.get('range').split('/', 1)[0]

        self.results['range'] = self._get_range(address)._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == '__main__':
    main()
