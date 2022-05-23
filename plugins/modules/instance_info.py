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

DOCUMENTATION = '''
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)
description:
- Get info about a Linode Instance.
module: instance_info
options:
  id:
    description:
    - "The instance\u2019s label."
    required: false
    type: int
  label:
    description:
    - The unique ID of the Instance.
    required: false
    type: str
requirements:
- python >= 3
'''

linode_instance_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False, doc_hide=True),

    id=dict(
        type='int', required=False,
        description=[
            'The instance’s label.'
        ]),

    label=dict(
        type='str', required=False,
        description=[
            'The unique ID of the Instance.'
        ])
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode Instance.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_instance_info_spec,
    examples=['''
- name: Get info about an instance by label
  linode.cloud.instance_info:
    label: 'my-instance' ''', '''
- name: Get info about an instance by id
  linode.cloud.instance_info:
    id: 12345'''],
    return_values=dict(
        instance=dict(
            description=['The instance description in JSON serialized form.'],
            docs_url='https://www.linode.com/docs/api/linode-instances/#linode-view__responses',
            type='dict',
            sample=['''{
  "alerts": {
    "cpu": 180,
    "io": 10000,
    "network_in": 10,
    "network_out": 10,
    "transfer_quota": 80
  },
  "backups": {
    "enabled": true,
    "last_successful": "2018-01-01T00:01:01",
    "schedule": {
      "day": "Saturday",
      "window": "W22"
    }
  },
  "created": "2018-01-01T00:01:01",
  "group": "Linode-Group",
  "hypervisor": "kvm",
  "id": 123,
  "image": "linode/debian10",
  "ipv4": [
    "203.0.113.1",
    "192.0.2.1"
  ],
  "ipv6": "c001:d00d::1337/128",
  "label": "linode123",
  "region": "us-east",
  "specs": {
    "disk": 81920,
    "memory": 4096,
    "transfer": 4000,
    "vcpus": 2
  },
  "status": "running",
  "tags": [
    "example tag",
    "another example"
  ],
  "type": "g6-standard-1",
  "updated": "2018-01-01T00:01:01",
  "watchdog_enabled": true
}''']
        ),
        configs=dict(
            description=['A list of configs tied to this Linode Instance.'],
            docs_url='https://www.linode.com/docs/api/linode-instances/#configuration-profile-view__responses',
            type='list',
            sample=['''[
  {
    "comments": "This is my main Config",
    "devices": {
      "sda": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdb": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdc": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdd": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sde": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdf": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdg": {
        "disk_id": 124458,
        "volume_id": null
      },
      "sdh": {
        "disk_id": 124458,
        "volume_id": null
      }
    },
    "helpers": {
      "devtmpfs_automount": false,
      "distro": true,
      "modules_dep": true,
      "network": true,
      "updatedb_disabled": true
    },
    "id": 23456,
    "interfaces": [
      {
        "ipam_address": "10.0.0.1/24",
        "label": "example-interface",
        "purpose": "vlan"
      }
    ],
    "kernel": "linode/latest-64bit",
    "label": "My Config",
    "memory_limit": 2048,
    "root_device": "/dev/sda",
    "run_level": "default",
    "virt_mode": "paravirt"
  }
]''']
        ),
        disks=dict(
            description=['A list of disks tied to this Linode Instance.'],
            docs_url='https://www.linode.com/docs/api/linode-instances/#disk-view__responses',
            type='list',
            sample=['''[
  {
    "created": "2018-01-01T00:01:01",
    "filesystem": "ext4",
    "id": 25674,
    "label": "Debian 9 Disk",
    "size": 48640,
    "status": "ready",
    "updated": "2018-01-01T00:01:01"
  }
]''']
        )
    )
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
