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

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_device as docs

MODULE_SPEC = dict(
    firewall_id=dict(
        type='int', required=True,
        description='The ID of the Firewall that contains this device.',
        ),

    entity_id=dict(
        type='int', required=True,
        description='The ID for this Firewall Device. This will be the ID of the Linode Entity.',
    ),

    entity_type=dict(
        type='str', required=True,
        description='The type of Linode Entity. Currently only supports linode.',
        choices=['linode'],
    ),

    label=dict(
        type='str',
        required=False,
        doc_hide=True,
    ),

    state=dict(type='str',
               description='The desired state of the target.',
               choices=['present', 'absent'], required=True),
)



specdoc_meta = dict(
    description=[
        'Manage Linode Firewall Devices.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=MODULE_SPEC,
    examples=docs.specdoc_examples,
    return_values=dict(
        device=dict(
            description='The Firewall Device in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/networking/#firewall-device-view__responses',
            type='dict',
            sample=docs.result_device_samples
        )
    )
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
            entity_id = params['entity_id']
            entity_type = params['entity_type']

            firewall = linode_api4.Firewall(self.client, firewall_id)
            for device in firewall.devices:
                if device.entity.id == entity_id and device.entity.type == entity_type:
                    return device

            return None
        except Exception as exception:
            return self.fail(msg='failed to get device {0}: {1}'.format(entity_id, exception))

    def _create_device(self) -> linode_api4.FirewallDevice:
        try:
            params = copy.deepcopy(self.module.params)

            firewall_id = params['firewall_id']
            entity_id = params['entity_id']
            entity_type = params['entity_type']

            firewall = linode_api4.Firewall(self.client, firewall_id)

            device = firewall.device_create(entity_id, entity_type, **params)
            self.register_action('Created Device {}: {}'.
                                 format(entity_id, device.created))

            return device
        except Exception as exception:
            return self.fail(msg='failed to create firewall device {0}: {1}'
                             .format(self.module.params.get('entity_id'), exception))

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
                                 .format(self.module.params.get('entity_id')))

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
