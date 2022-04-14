#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

# pylint: disable=unused-import
import copy
from typing import Optional, Any, List

import linode_api4
from linode_api4 import Domain

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

MODULE_SPEC = dict(
    firewall_id=dict(
        type='int', required=True,
        description='The ID of the Firewall that contains this device.',
        ),

    device_id=dict(
        type='int', required=True,
        description='The ID for this Firewall Device. This will be the ID of the Linode Entity.',
    ),

    device_type=dict(
        type='str', required=True,
        description='The type of Linode Entity. Currently only supports linode.',
        choices=['linode'],
    ),

    label=dict(
        type='str',
        required=False,
        doc_hide=True,
    )
)

specdoc_meta = dict(
    description=[
        'Manage Linode Firewall Devices.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=MODULE_SPEC
)

class LinodeFirewallDevice(LinodeModuleBase):
    """Module for managing Linode Firewall devices"""

    def __init__(self) -> None:
        self.module_arg_spec = MODULE_SPEC
        self.required_one_of: List[str] = []
        self.results = dict(
            changed=False,
            actions=[],
            device=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def _get_device(self) -> Optional[linode_api4.FirewallDevice]:
        try:
            params = self.module.params
            firewall_id = params['firewall_id']
            device_id = params['device_id']

            firewall = linode_api4.Firewall(self.client, firewall_id)
            for device in firewall.devices:
                if device.id == device_id:
                    return device

            return None
        except Exception as exception:
            return self.fail(msg='failed to get device {0}: {1}'.format(device_id, exception))

    def _create_device(self) -> linode_api4.FirewallDevice:
        try:
            params = copy.deepcopy(self.module.params)

            firewall_id = params['firewall_id']
            device_id = params['device_id']
            device_type = params['device_type']

            firewall = linode_api4.Firewall(self.client, firewall_id)

            device = firewall.device_create(device_id, device_type, **params)
            self.register_action('Created Device {}: {}'.
                                 format(device_id, device.created))

            return device
        except Exception as exception:
            return self.fail(msg='failed to create firewall device {0}: {1}'
                             .format(self.module.params.get('device_id'), exception))

    def _handle_present(self) -> None:
        device = self._get_device()

        # Create the device if it does not already exist
        if device is None:
            device = self._create_device()

        # Force lazy-loading
        device._api_get()

        self.results['device'] = device._raw_json

    def _handle_absent(self) -> None:
        device = self._get_device()

        if device is not None:
            self.results['device'] = device._raw_json

            device.delete()
            self.register_action('Deleted firewall device {0}'
                                 .format(self.module.params.get('device_id')))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for firewall_device module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results

def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeFirewallDevice()


if __name__ == '__main__':
    main()

DOCUMENTATION='''
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)
description:
- Manage Linode Firewall Devices.
module: firewall_device
options:
  device_id:
    description: The ID for this Firewall Device. This will be the ID of the Linode
      Entity.
    required: true
    type: int
  device_type:
    choices:
    - linode
    description: The type of Linode Entity. Currently only supports linode.
    required: true
    type: str
  firewall_id:
    description: The ID of the Firewall that contains this device.
    required: true
    type: int
requirements:
- python >= 3
'''

EXAMPLES = '''
- name: Create a Firewall
  linode.cloud.firewall:
    label: my-firewall
    rules:
      inbound_policy: DROP
    state: present
  register: firewall_result

- name: Create an Instance
  linode.cloud.instance:
    label: my-instance
    region: us-east
    private_ip: true
    type: g6-standard-1
    state: present
  register: instance_result

- name: Attach the instance to the Firewall
  linode.cloud.firewall_device:
    firewall_id: '{{ firewall_result.firewall.id }}'
    device_id: '{{ instance_result.instance.id }}'
    device_type: 'linode'
    state: present
'''

RETURN = '''
device:
  description: The Firewall Device in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/networking/#firewall-device-view__response-samples"
  returned: always
  type: dict
  sample: {
        "created": "2018-01-01T00:01:01",
        "entity": {
            "id": 123,
            "label": "my-linode",
            "type": "linode",
            "url": "/v4/linode/instances/123"
        },
        "id": 123,
        "updated": "2018-01-02T00:01:01"
    }
'''
