#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode databases."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import Any, Optional, Dict

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    filter_null_values, construct_api_filter, get_all_paginated
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_list as docs

spec_filter = dict(
    name=dict(type='str', required=True,
              description=[
                  'The name of the field to filter on.',
                  'Valid filterable attributes can be found here: '
                  'https://www.linode.com/docs/api/databases/'
                  '#managed-mongodb-databases-list__responses',
              ]),
    values=dict(type='list', elements='str', required=True,
                description=[
                    'A list of values to allow for this field.',
                    'Fields will pass this filter if at least one of these values matches.'
                ])
)

spec = dict(
    # Disable the default values
    state=dict(type='str', required=False, doc_hide=True),
    label=dict(type='str', required=False, doc_hide=True),

    order=dict(type='str', description='The order to list databases in.',
               default='asc', choices=['desc', 'asc']),
    order_by=dict(type='str', description='The attribute to order databases by.'),
    filters=dict(type='list', elements='dict', options=spec_filter,
                 description='A list of filters to apply to the resulting databases.'),
    count=dict(type='int',
               description=[
                   'The number of results to return.',
                   'If undefined, all results will be returned.'])
)

specdoc_meta = dict(
    description=[
        'List and filter on Linode Managed Databases.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        databases=dict(
            description='The returned database.',
            docs_url='https://www.linode.com/docs/api/databases/'
                     '#managed-databases-list-all__response-samples',
            type='list',
            elements='dict',
            sample=docs.result_images_samples
        )
    )
)


class Module(LinodeModuleBase):
    """Module for getting info about a Linode databases"""

    def __init__(self) -> None:
        self.module_arg_spec = spec
        self.results: Dict[str, Any] = {
            'databases': []
        }

        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for database list module"""

        filter_dict = construct_api_filter(self.module.params)

        self.results['databases'] = get_all_paginated(self.client, '/databases/instances', filter_dict,
                                                      num_results=self.module.params['count'])
        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == '__main__':
    main()
