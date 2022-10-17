#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode IP address."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import Image, IPAddress

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    filter_null_values
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_info as docs

spec = dict(
    # Disable the default values
    state=dict(type='str', required=False, doc_hide=True),
    label=dict(type='str', required=False, doc_hide=True),

    address=dict(type='str', required=True,
                 description='The IP address to operate on.'),
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode IP.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        ip=dict(
            description='The IP in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/networking/#ip-address-view__responses',
            type='dict',
            sample=docs.result_ip_samples
        )
    )
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.module_arg_spec = spec
        self.results = {
            'ip': None
        }

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=[],
                         mutually_exclusive=[])

    def _get_ip(self, ip: str) -> IPAddress:
        try:
            ip = IPAddress(self.client, ip)

            ip._api_get()

            return ip
        except Exception as exception:
            self.fail(msg='failed to get IP address {0}: {1}'.format(ip, exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ip_info module"""

        params = filter_null_values(self.module.params)

        address = params.get('address')
        ip = self._get_ip(address)

        self.results['ip'] = ip._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == '__main__':
    main()
