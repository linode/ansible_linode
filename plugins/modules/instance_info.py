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
  
configs:
  description: The configs tied to this Linode instance.
  linode_api_docs: "https://www.linode.com/docs/api/linode-instances/#configuration-profile-view__responses"
  returned: always
  type: list
  sample: [
   {
      "comments":"",
      "created":"xxxxx",
      "devices":{
         "sda":null,
         "sdb":{
            "disk_id":xxxxx,
            "volume_id":null
         },
         "sdc":null,
         "sdd":null,
         "sde":null,
         "sdf":null,
         "sdg":null,
         "sdh":null
      },
      "helpers":{
         "devtmpfs_automount":true,
         "distro":true,
         "modules_dep":true,
         "network":true,
         "updatedb_disabled":true
      },
      "id":xxxxx,
      "initrd":null,
      "interfaces":[
         
      ],
      "kernel":"linode/grub2",
      "label":"My Ubuntu 20.04 LTS Disk Profile",
      "memory_limit":0,
      "root_device":"/dev/sda",
      "run_level":"default",
      "updated":"xxxxx",
      "virt_mode":"paravirt"
   }
]

disks:
  description: The disks tied to this Linode instance.
  linode_api_docs: "https://www.linode.com/docs/api/linode-instances/#disk-view"
  returned: always
  type: list
  sample: [
  {
    "created": "xxxxx",
    "filesystem": "ext4",
    "id": xxxxx,
    "label": "test-disk",
    "size": 10,
    "status": "ready",
    "updated": "xxxxx"
  }
]
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

    def __get_matching_instance(self) -> Optional[Instance]:
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

        instance = self.__get_matching_instance()

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
