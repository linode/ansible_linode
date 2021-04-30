#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Firewall info."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from linode_api4 import Firewall

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    paginated_list_to_json

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
---
module: firewall_info
description: Get info about a Linode Firewall. \
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
      - The Firewall’s label.
    type: string
  id:
    description:
      - The unique id of the Firewall.
    type: int
'''

EXAMPLES = '''
- name: Get info about a Firewall by label
  linode.cloud.firewall_info:
    label: 'my-firewall'

- name: Get info about a Firewall by id
  linode.cloud.firewall_info:
    id: 12345
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

linode_firewall_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False),

    id=dict(type='int', required=False),
    label=dict(type='str', required=False)
)

linode_firewall_valid_filters = [
    'id', 'label'
]


class LinodeFirewallInfo(LinodeModuleBase):
    """Configuration class for Linode Firewall resource"""

    def __init__(self):
        self.module_arg_spec = linode_firewall_info_spec
        self.required_one_of = []
        self.results = dict(
            firewall=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def get_firewall_by_properties(self, **kwargs):
        """Gets the Firewall with the given property in kwargs"""

        filter_items = {k: v for k, v in kwargs.items()
                        if k in linode_firewall_valid_filters and v is not None}

        filter_statement = create_filter_and(Firewall, filter_items)

        try:
            # Special case because ID is not filterable
            if 'id' in filter_items.keys():
                result = Firewall(self.client, kwargs.get('id'))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.networking.firewalls(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get firewall {0}'.format(exception))

    def exec_module(self, **kwargs):
        """Entrypoint for Firewall info module"""

        firewall = self.get_firewall_by_properties(**kwargs)

        if firewall is None:
            self.fail('failed to get firewall')

        self.results['firewall'] = firewall._raw_json
        self.results['devices'] = paginated_list_to_json(firewall.devices)

        return self.results


def main():
    """Constructs and calls the Linode Firewall info module"""
    LinodeFirewallInfo()


if __name__ == '__main__':
    main()
