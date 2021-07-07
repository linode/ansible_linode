#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Firewalls."""

from __future__ import absolute_import, division, print_function

import copy
from typing import Optional, List, Any

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    filter_null_values, mapping_to_dict, paginated_list_to_json

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
---
module: firewall
description: 
  - Manage Linode Firewalls. \
This endpoint is currently in beta and will only function \
correctly if `api_version` is set to `v4beta`. 
requirements:
  - python >= 2.7
  - linode_api4 >= 5.1.0
author:
  - Luke Murphy (@decentral1se)
  - Charles Kenney (@charliekenney23)
  - Phillip Campbell (@phillc)
  - Lena Garber (@lbgarber)
options:
  label:
    description:
      - The unique label to give this Firewall.
    required: true
    type: str
    
  status:
    description:
      - The status of this Firewall.
    type: str
    choices:
      - enabled
      - disabled
      - deleted

  devices:
    description:
      - The devices that are attached to this Firewall.
    type: list
    elements: dict
    suboptions:
        id:
          description:
            - The unique ID of the device to attach to this Firewall.
          type: str
          required: true
        type:
          description:
            - The type of device to be attached to this Firewall.
          type: str
          choices:
            - linode
          default: linode
          
  rules:
    description:
      - The inbound and outbound access rules to apply to the Firewall.
    type: dict
    suboptions:
      inbound_policy:
        description:
          - The default behavior for inbound traffic.
        type: str
        required: true
        choices:
          - ACCEPT
          - DROP
        
      outbound_policy:
        description:
          - The default behavior for outbound traffic.
        type: str
        required: true
        choices:
          - ACCEPT
          - DROP
          
      inbound:
        description:
          - A list of rules for inbound traffic.
        type: list
        elements: dict
        suboptions:
          label:
            description:
              - The label of this rule.
            type: str
            required: true
          action:
            description:
              - Controls whether traffic is accepted or dropped by this rule.
            type: str
            choices:
              - ACCEPT
              - DROP
            required: true
          description:
            description:
              - The description of this rule.
            type: str
          addresses:
            description:
              - Allowed IPv4 or IPv6 addresses.
            type: list
            elements: dict
            suboptions:
              ipv4:
                description:
                  - A list of IPv4 addresses or networks. 
                  - Must be in IP/mask format.
                type: list
                elements: str
              ipv6:
                description:
                  - A list of IPv4 addresses or networks. 
                  - Must be in IP/mask format.
                type: list
                elements: str
            ports:
              description:
                - A string representing the port or ports on which traffic will be allowed.
                - See U(https://www.linode.com/docs/api/networking/#firewall-create)
              type: str
            protocol:
              description:
                - The type of network traffic to allow.
              type: str
              choices:
                - TCP
                - UDP
                - ICMP
                
      outbound:
        description:
          - A list of rules for outbound traffic.
        type: list
        elements: dict
        suboptions:
          label:
            description:
              - The label of this rule.
            type: str
            required: true
          action:
            description:
              - Controls whether traffic is accepted or dropped by this rule.
            type: str
            choices:
              - ACCEPT
              - DROP
            required: true
          description:
            description:
              - The description of this rule.
            type: str
          addresses:
            description:
              - Allowed IPv4 or IPv6 addresses.
            type: list
            elements: dict
            suboptions:
              ipv4:
                description:
                  - A list of IPv4 addresses or networks. 
                  - Must be in IP/mask format.
                type: list
                elements: str
              ipv6:
                description:
                  - A list of IPv4 addresses or networks. 
                  - Must be in IP/mask format.
                type: list
                elements: str
            ports:
              description:
                - A string representing the port or ports on which traffic will be allowed.
                - See U(https://www.linode.com/docs/api/networking/#firewall-create)
              type: str
            protocol:
              description:
                - The type of network traffic to allow.
              type: str
              choices:
                - TCP
                - UDP
                - ICMP
'''

EXAMPLES = '''
- name: Create a Linode Firewall
  linode.cloud.firewall:
    api_version: v4beta
    label: 'my-firewall'
    devices:
      - id: 123
        type: linode
    rules:
      inbound_policy: DROP
      inbound:
        - label: allow-http-in
          addresses:
            ipv4:
              - 0.0.0.0/0
            ipv6:
              - 'ff00::/8'
          description: Allow inbound HTTP and HTTPS connections.
          ports: '80,443'
          protocol: TCP
          action: ACCEPT

      outbound_policy: DROP
      outbound:
        - label: allow-http-out
          addresses:
            ipv4:
              - 0.0.0.0/0
            ipv6:
              - 'ff00::/8'
          description: Allow outbound HTTP and HTTPS connections.
          ports: '80,443'
          protocol: TCP
          action: ACCEPT
    state: present
    
- name: Delete a Linode Firewall
  linode.cloud.firewall:
    api_version: v4beta
    label: 'my-firewall'
    state: absent
'''

RETURN = '''
firewall:
  description: The Firewall description in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/networking/#firewall-view"
  returned: always
  type: dict
  sample: {
   "created":"xxxxx",
   "updated":"xxxxx",
   "status":"enabled",
   "id":xxxx,
   "label":"my-firewall",
   "rules":{
      "inbound":[
         {
            "action":"ACCEPT",
            "addresses":{
               "ipv4":[
                  "0.0.0.0/0"
               ],
               "ipv6":[
                  "ff00::/8"
               ]
            },
            "description":"Allow inbound HTTP and HTTPS connections.",
            "label":"allow-http-in",
            "ports":"80,443",
            "protocol":"TCP"
         }
      ],
      "inbound_policy":"DROP",
      "outbound":[
         {
            "action":"ACCEPT",
            "addresses":{
               "ipv4":[
                  "0.0.0.0/0"
               ],
               "ipv6":[
                  "ff00::/8"
               ]
            },
            "description":"Allow outbound HTTP and HTTPS connections.",
            "label":"allow-http-out",
            "ports":"80,443",
            "protocol":"TCP"
         }
      ],
      "outbound_policy":"DROP"
   }
}
devices:
  description: A list of Firewall devices JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/networking/#firewall-device-view"
  returned: always
  type: list
  sample: [
   {
      "created":"xxxxxx",
      "entity":{
         "id":xxxxxx,
         "label":"my-device",
         "type":"linode",
         "url":"/v4/linode/instances/xxxxxx"
      },
      "id":xxxxxx,
      "updated":"xxxxxx"
   }
]
'''

try:
    from linode_api4 import Firewall, FirewallDevice
except ImportError:
    # handled in module_utils.linode_common
    pass

linode_firewall_addresses_spec: dict = dict(
    ipv4=dict(type='list', elements='str'),
    ipv6=dict(type='list', elements='str')
)

linode_firewall_rule_spec: dict = dict(
    label=dict(type='str', required=True),
    action=dict(type='str', required=True),
    addresses=dict(type='dict', options=linode_firewall_addresses_spec),
    description=dict(type='str'),
    ports=dict(type='str'),
    protocol=dict(type='str')
)

linode_firewall_rules_spec: dict = dict(
    inbound=dict(type='list', elements='dict', options=linode_firewall_rule_spec),
    inbound_policy=dict(type='str'),
    outbound=dict(type='list', elements='dict', options=linode_firewall_rule_spec),
    outbound_policy=dict(type='str'),
)

linode_firewall_device_spec: dict = dict(
    id=dict(type='int', required=True),
    type=dict(type='str', default='linode')
)

linode_firewall_spec: dict = dict(
    label=dict(type='str'),
    devices=dict(type='list', elements='dict', options=linode_firewall_device_spec),
    rules=dict(type='dict', options=linode_firewall_rules_spec),
    status=dict(type='str')
)

# Fields that can be updated on an existing Firewall
linode_firewall_mutable: List[str] = [
    'status',
    'tags'
]


class LinodeFirewall(LinodeModuleBase):
    """Module for creating and destroying Linode Firewalls"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_firewall_spec

        self.results: dict = dict(
            changed=False,
            actions=[],
            firewall=None,
            devices=None
        )

        self._firewall: Optional[Firewall] = None

        super().__init__(module_arg_spec=self.module_arg_spec)

    def _get_firewall_by_label(self, label: str) -> Optional[Firewall]:
        try:
            return self.client.networking.firewalls(Firewall.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get firewall {0}: {1}'.format(label, exception))

    def _create_firewall(self) -> dict:
        params = copy.deepcopy(self.module.params)

        label = params.pop('label')
        params = {k: v for k, v in params.items() if k in {
            'rules', 'tags'
        }}

        try:
            result = self.client.networking.firewall_create(label, **params)
        except Exception as exception:
            self.fail(msg='failed to create firewall: {0}'.format(exception))

        return result

    def _create_device(self, device_id: int, device_type: str, **spec_args: Any) -> None:
        self._firewall.device_create(device_id, device_type, **spec_args)
        self.register_action('Created device {0} of type {1}'.format(
            device_id, device_type))

    def _delete_device(self, device: FirewallDevice) -> None:
        self.register_action('Deleted device {0} of type {1}'.format(
            device.entity.id, device.entity.type))
        device.delete()

    def _update_devices(self, spec_devices: list) -> None:
        # Remove devices that are not present in config
        device_map = {}

        for device in self._firewall.devices:
            device_map[device.entity.id] = device

        # Handle creating/keeping existing devices
        for device in spec_devices:
            device_entity_id = device.get('id')
            device_entity_type = device.get('type')

            if device_entity_id in device_map:
                if device_map[device_entity_id].entity.type == device_entity_type:
                    del device_map[device_entity_id]
                    continue

                # Recreate the device if the fields don't match
                self._delete_device(device_map[device_entity_id])

            self._create_device(device_entity_id, device_entity_type)

        # Delete unused devices
        for device in device_map.values():
            self._delete_device(device)

    def _update_firewall(self) -> None:
        """Handles all update functionality for the current Firewall"""

        # Update mutable values
        should_update = False
        params = filter_null_values(self.module.params)

        for key, new_value in params.items():
            if not hasattr(self._firewall, key):
                continue

            old_value = getattr(self._firewall, key)

            if new_value != old_value:
                if key in linode_firewall_mutable:
                    setattr(self._firewall, key, new_value)
                    self.register_action('Updated Firewall {0}: "{1}" -> "{2}"'.
                                         format(key, old_value, new_value))

                    should_update = True

        if should_update:
            self._firewall.save()

        # Update rules
        if mapping_to_dict(self._firewall.rules) != params.get('rules'):
            self._firewall.update_rules(params.get('rules'))
            self.register_action('Updated Firewall rules')

        # Update devices
        devices: Optional[List[Any]] = params.get('devices')
        if devices is not None:
            self._update_devices(devices)

    def _handle_firewall(self) -> None:
        """Updates the Firewall"""
        label = self.module.params.get('label')

        self._firewall = self._get_firewall_by_label(label)

        if self._firewall is None:
            self._firewall = self._create_firewall()
            self.register_action('Created Firewall {0}'.format(label))

        self._update_firewall()

        self._firewall._api_get()

        self.results['firewall'] = self._firewall._raw_json
        self.results['devices'] = paginated_list_to_json(self._firewall.devices)

    def _handle_firewall_absent(self) -> None:
        """Destroys the Firewall"""
        label = self.module.params.get('label')

        self._firewall = self._get_firewall_by_label(label)

        if self._firewall is not None:
            self.results['firewall'] = self._firewall._raw_json
            self.results['devices'] = paginated_list_to_json(self._firewall.devices)
            self.register_action('Deleted Firewall {0}'.format(label))
            self._firewall.delete()

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Firewall module"""

        state = kwargs.get('state')

        if state == 'absent':
            self._handle_firewall_absent()
            return self.results

        self._handle_firewall()
        return self.results


def main() -> None:
    """Constructs and calls the Linode Firewall module"""

    LinodeFirewall()


if __name__ == '__main__':
    main()
