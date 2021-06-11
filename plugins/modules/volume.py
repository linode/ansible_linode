#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Volumes."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import Optional, cast, Any

from linode_api4 import Volume

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
---
module: volume
description: Manage Linode volumes.
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
      - The Volume’s label, which is also used in the filesystem_path of the resulting volume.
    required: true
    type: string
  region:
    description:
      - The location to deploy the volume in.
      - See U(https://api.linode.com/v4/regions)
    type: str
  size:
    description:
      - The size of this volume, in GB. 
      - Be aware that volumes may only be resized up after creation.
    type: int
  linode_id:
    description:
      - The Linode this volume should be attached to upon creation. 
      - If not given, the volume will be created without an attachment.
    type: int
  config_id:
    description:
      - When creating a Volume attached to a Linode, the ID of the Linode Config to include the new Volume in.
    type: int
  attached:
    description:
      - If true, the volume will be attached to a Linode. Otherwise, the volume will be detached.
    type: bool
'''

EXAMPLES = '''
- name: Create a volume attached to an instance
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    linode_id: 12345
    state: present
    
- name: Create an unattached volume
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    state: present
    
- name: Resize a volume
  linode.cloud.volume:
    label: example-volume
    size: 50
    state: present
    
- name: Detach a volume
  linode.cloud.volume:
    label: example-volume
    attached: false
    state: present
    
- name: Delete a volume
  linode.cloud.volume:
    label: example-volume
    state: absent
'''

RETURN = '''
volume:
  description: The volume in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/volumes/#volume-view__responses"
  returned: always
  type: dict
  sample: {
   "created":"",
   "filesystem_path":"/dev/disk/by-id/xxxxxx",
   "id":xxxxxx,
   "label":"xxxxxx",
   "linode_id":xxxxxx,
   "linode_label":"xxxxxx",
   "region":"us-east",
   "size":30,
   "status":"creating",
   "tags":[],
   "updated":"2021-03-05T19:05:33"
}
'''

linode_volume_spec = dict(
    config_id=dict(type='int', required=False, default=None),
    linode_id=dict(type='int', required=False, default=None),
    region=dict(type='str', required=False),
    size=dict(type='int', required=False, default=None),
    attached=dict(type='bool', required=False, default=True)
)


class LinodeVolume(LinodeModuleBase):
    """Module for creating and destroying Linode Volumes"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_volume_spec
        self.required_one_of = ['state', 'label']
        self.results = dict(
            changed=False,
            actions=[],
            volume=None,
        )

        self._volume: Optional[Volume] = None

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def __get_volume_by_label(self, label: str) -> Optional[Volume]:
        try:
            return self.client.volumes(Volume.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get volume {0}: {1}'.format(label, exception))

    def __create_volume(self) -> Optional[Volume]:
        params = self.module.params
        label = params.pop('label')
        region = params.pop('region')
        linode_id = params.pop('linode_id')
        size = params.pop('size')

        try:
            return self.client.volume_create(label, region, linode_id, size, **params)
        except Exception as exception:
            return self.fail(msg='failed to create volume: {0}'.format(exception))

    def __handle_volume(self) -> None:
        params = self.module.params

        label: str = params.get('label')
        size: int = params.get('size')
        linode_id: int = params.get('linode_id')
        config_id: int = params.get('config_id')
        attached: bool = params.pop('attached')

        self._volume = self.__get_volume_by_label(label)

        # Create the volume if it does not already exist
        if self._volume is None:
            self._volume = self.__create_volume()
            self.register_action('Created volume {0}'.format(label))

        # Resize the volume if its size does not match
        if size is not None and self._volume.size != size:
            self._volume.resize(size)
            self.register_action('Resized volume {0} to size {1}'
                                 .format(label, size))

        # Attach the volume to a Linode
        if linode_id is not None and self._volume.linode_id != linode_id:
            self._volume.attach(linode_id, config_id)
            self.register_action(
                'Attached volume {0} to linode_id {1} and config_id {2}'
                    .format(label, linode_id, config_id))

        if not attached:
            self._volume.detach()
            self.register_action(
                'Detached volume {0}'.format(label)
            )

        # Force lazy-loading
        self._volume._api_get()

        self.results['volume'] = self._volume._raw_json

    def __handle_volume_absent(self) -> None:
        label: str = self.module.params.get('label')

        self._volume = self.__get_volume_by_label(label)

        if self._volume is not None:
            self.results['volume'] = self._volume._raw_json
            self._volume.delete()
            self.register_action('Deleted volume {0}'.format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for volume module"""
        state = kwargs.get('state')

        if state == 'absent':
            self.__handle_volume_absent()
            return self.results

        self.__handle_volume()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Volume module"""
    LinodeVolume()


if __name__ == '__main__':
    main()
