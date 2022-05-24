#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Volumes."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import Optional, cast, Any, Set

import polling
from linode_api4 import Volume

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

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
    label=dict(
        type='str',
        description='The Volume’s label, which is also used in the '
                    'filesystem_path of the resulting volume.'),

    config_id=dict(
        type='int', default=None,
        description='When creating a Volume attached to a Linode, the ID of the Linode Config '
                    'to include the new Volume in.'),

    linode_id=dict(
        type='int', default=None,
        description=[
            'The Linode this volume should be attached to upon creation.',
            'If not given, the volume will be created without an attachment.'
        ]),

    region=dict(
        type='str',
        description=[
            'The location to deploy the volume in.',
            'See U(https://api.linode.com/v4/regions)'
        ]),

    size=dict(
        type='int', default=None,
        description=[
            'The size of this volume, in GB.',
            'Be aware that volumes may only be resized up after creation.'
        ]),

    attached=dict(
        type='bool', default=True,
        description='If true, the volume will be attached to a Linode. '
                    'Otherwise, the volume will be detached.'),

    wait_timeout=dict(
        type='int', default=240,
        description='The amount of time, in seconds, to wait for a volume to '
                    'have the active status.'
        ),

    state=dict(type='str',
               description='The desired state of the target.',
               choices=['present', 'absent'], required=True),
)

specdoc_examples = ['''
- name: Create a volume attached to an instance
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    linode_id: 12345
    state: present''', '''
- name: Create an unattached volume
  linode.cloud.volume:
    label: example-volume
    region: us-east
    size: 30
    state: present''', '''
- name: Resize a volume
  linode.cloud.volume:
    label: example-volume
    size: 50
    state: present''', '''
- name: Detach a volume
  linode.cloud.volume:
    label: example-volume
    attached: false
    state: present''', '''
- name: Delete a volume
  linode.cloud.volume:
    label: example-volume
    state: absent''']

result_volume_samples = ['''{
  "created": "2018-01-01T00:01:01",
  "filesystem_path": "/dev/disk/by-id/scsi-0Linode_Volume_my-volume",
  "hardware_type": "nvme",
  "id": 12345,
  "label": "my-volume",
  "linode_id": 12346,
  "linode_label": "linode123",
  "region": "us-east",
  "size": 30,
  "status": "active",
  "tags": [
    "example tag",
    "another example"
  ],
  "updated": "2018-01-01T00:01:01"
}''']

specdoc_meta = dict(
    description=[
        'Manage a Linode Volume.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_volume_spec,
    examples=specdoc_examples,
    return_values=dict(
        volume=dict(
            description='The volume in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/volumes/#volume-view__responses',
            type='dict',
            sample=result_volume_samples
        )
    )
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

    def _get_volume_by_label(self, label: str) -> Optional[Volume]:
        try:
            return self.client.volumes(Volume.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get volume {0}: {1}'.format(label, exception))

    def _create_volume(self) -> Optional[Volume]:
        params = self.module.params
        label = params.pop('label')
        region = params.pop('region')
        linode_id = params.pop('linode_id')
        size = params.pop('size')

        try:
            return self.client.volume_create(label, region, linode_id, size, **params)
        except Exception as exception:
            return self.fail(msg='failed to create volume: {0}'.format(exception))

    def _wait_for_volume_status(self, volume: Volume, status: Set[str], timeout: int) -> None:
        def poll_func() -> bool:
            volume._api_get()
            return volume.status in status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=5,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail('failed to wait for volume status: timeout period expired')

    def _wait_for_volume_active(self) -> None:
        self._wait_for_volume_status(self._volume, {'active'},
                                     self.module.params.get('wait_timeout'))

    def _handle_volume(self) -> None:
        params = self.module.params

        label: str = params.get('label')
        size: int = params.get('size')
        linode_id: int = params.get('linode_id')
        config_id: int = params.get('config_id')
        attached: bool = params.pop('attached')

        self._volume = self._get_volume_by_label(label)

        # Create the volume if it does not already exist
        if self._volume is None:
            self._volume = self._create_volume()
            self.register_action('Created volume {0}'.format(label))

        # Ensure volume is active before continuing
        self._wait_for_volume_active()

        # Resize the volume if its size does not match
        if size is not None and self._volume.size != size:
            self._volume.resize(size)
            self.register_action('Resized volume {0} to size {1}'
                                 .format(label, size))

            # Wait for resize to complete
            self._wait_for_volume_active()

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

    def _handle_volume_absent(self) -> None:
        label: str = self.module.params.get('label')

        self._volume = self._get_volume_by_label(label)

        if self._volume is not None:
            self.results['volume'] = self._volume._raw_json
            self._volume.delete()
            self.register_action('Deleted volume {0}'.format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for volume module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_volume_absent()
            return self.results

        self._handle_volume()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Volume module"""
    LinodeVolume()


if __name__ == '__main__':
    main()
