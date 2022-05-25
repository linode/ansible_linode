#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Instance info."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Optional, Any, Dict

from linode_api4 import Instance

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    paginated_list_to_json
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

from ansible_collections.linode.cloud.plugins.modules.instance import specdoc_meta \
    as instance_specdoc_meta

linode_instance_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False, doc_hide=True),

    id=dict(
        type='int', required=False,
        description=[
            'The instance’s label.',
            'Optional if `label` is defined.'
        ]),

    label=dict(
        type='str', required=False,
        description=[
            'The unique ID of the Instance.',
            'Optional if `id` is defined.'
        ])
)

specdoc_examples = ['''
- name: Get info about an instance by label
  linode.cloud.instance_info:
    label: 'my-instance' ''', '''
- name: Get info about an instance by id
  linode.cloud.instance_info:
    id: 12345''']

specdoc_meta = dict(
    description=[
        'Get info about a Linode Instance.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_instance_info_spec,
    examples=specdoc_examples,
    return_values=instance_specdoc_meta['return_values']
)

linode_instance_valid_filters = [
    'id', 'label'
]

class LinodeInstanceInfo(LinodeModuleBase):
    """Module for getting info about a Linode Instance"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_instance_info_spec
        self.required_one_of: List[str] = []
        self.results: Dict[str, Any] = dict(
            instance=None,
            configs=None,
            disks=None
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def _get_matching_instance(self) -> Optional[Instance]:
        params = self.module.params

        filter_items = {k: v for k, v in params.items()
                        if k in linode_instance_valid_filters and v is not None}

        filter_statement = create_filter_and(Instance, filter_items)

        try:
            # Special case because ID is not filterable
            if 'id' in filter_items.keys():
                result = Instance(self.client, params.get('id'))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.linode.instances(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get instance {0}'.format(exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for instance info module"""

        instance = self._get_matching_instance()

        if instance is None:
            return self.fail('failed to get instance')

        self.results['instance'] = instance._raw_json
        self.results['configs'] = paginated_list_to_json(instance.configs)
        self.results['disks'] = paginated_list_to_json(instance.disks)

        return self.results


def main() -> None:
    """Constructs and calls the Linode Instance info module"""
    LinodeInstanceInfo()


if __name__ == '__main__':
    main()
