#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode VLAN info."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Optional, Any

from linode_api4 import VLAN

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
---
module: vlan_info
description: Get info about a Linode VLAN. \
This endpoint is currently in beta and will only function correctly if `api_version` is set to `v4beta`.
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
      - The VLAN’s label.
    type: string
'''

EXAMPLES = '''
- name: Get info about a VLAN by label
  linode.cloud.vlan_info:
    label: example-vlan
'''

RETURN = '''
vlan:
  description: The VLAN in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/networking/#vlans-list__response-samples"
  returned: always
  type: dict
  sample: {
   "created":"xxxxx",
   "label":"example-vlan",
   "linodes":[
      12345
   ],
   "region":"us-southeast"
}
'''

linode_vlan_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False),

    label=dict(type='str', required=True)
)


class LinodeVLANInfo(LinodeModuleBase):
    """Configuration class for Linode VLAN resource"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_vlan_info_spec
        self.required_one_of: List[str] = []
        self.results = dict(
            vlan=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def get_vlan_by_label(self, label: str) -> Optional[VLAN]:
        """Gets the VLAN with the given property in kwargs"""

        try:
            return self.client.networking.vlans(VLAN.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get VLAN {0}'.format(exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for VLAN info module"""

        label: str = kwargs.get('label')

        vlan = self.get_vlan_by_label(label)

        if vlan is None:
            self.fail('failed to get vlan')

        self.results['vlan'] = vlan._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the Linode VLAN info module"""
    LinodeVLANInfo()


if __name__ == '__main__':
    main()
