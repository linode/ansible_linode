#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Instance info."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from linode_api4 import Instance

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
---
module: instance_info
description: Get info about a Linode instance.
requirements:
  - python >= 2.7
  - linode_api4 >= 3.0
author:
  - Luke Murphy (@decentral1se)
  - Charles Kenney (@charliekenney23)
  - Phillip Campbell (@phillc)
  - Lena Garber (@lbgarber)
options:
  label:
    description:
      - The instance’s label.
    type: string
  id:
    description:
      - The unique id of the instance.
    type: int
'''

EXAMPLES = '''
- name: Get info about an instance by label
  linode.cloud.instance_info:
    label: 'my-instance'
    
- name: Get info about an instance by id
  linode.cloud.instance_info:
    id: 12345
'''

RETURN = '''
instance:
  description: The instance description in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/linode-instances/#linode-view__responses"
  returned: always
  type: dict
  sample: {
    "alerts": {
      "cpu": 90,
      "io": 10000,
      "network_in": 10,
      "network_out": 10,
      "transfer_quota": 80
    },
    "backups": {
      "enabled": false,
      "schedule": {
        "day": null,
        "window": null
      }
    },
    "created": "xxxx-xx-xxTxx:xx:xx",
    "group": "app",
    "hypervisor": "kvm",
    "id": xxxxxx,
    "image": "linode/ubuntu20.04",
    "ipv4": [
      "xxx.xxx.xxx.xxx"
    ],
    "ipv6": "xxxx:xxxx::xxxx:xxxx:xxxx:xxxx/64",
    "label": "my-linode",
    "region": "us-east",
    "specs": {
      "disk": 25600,
      "memory": 1024,
      "transfer": 1000,
      "vcpus": 1
    },
    "status": "running",
    "tags": ["env=prod"],
    "type": "g6-nanode-1",
    "updated": "xxxx-xx-xxTxx:xx:xx",
    "watchdog_enabled": true
  }
'''

linode_instance_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False),

    id=dict(type='int', required=False),
    label=dict(type='str', required=False)
)

linode_instance_valid_filters = [
    'id', 'label'
]

class LinodeInstanceInfo(LinodeModuleBase):
    """Configuration class for Linode instance resource"""

    def __init__(self):
        self.module_arg_spec = linode_instance_info_spec
        self.required_one_of = []
        self.results = dict(
            Instance=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def get_instance_by_properties(self, **kwargs):
        """Gets the instance with the given property in kwargs"""

        filter_items = {k: v for k, v in kwargs.items()
                        if k in linode_instance_valid_filters and v is not None}

        filter_statement = create_filter_and(Instance, filter_items)

        try:
            # Special case because ID is not filterable
            if 'id' in filter_items.keys():
                result = Instance(self.client, kwargs.get('id'))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.linode.instances(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get instance {0}'.format(exception))

    def exec_module(self, **kwargs):
        """Entrypoint for instance info module"""

        instance = self.get_instance_by_properties(**kwargs)

        if instance is None:
            self.fail('failed to get instance')

        self.results['instance'] = instance._raw_json

        return self.results


def main():
    """Constructs and calls the Linode Instance info module"""
    LinodeInstanceInfo()


if __name__ == '__main__':
    main()
