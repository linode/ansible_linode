#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode instances."""

from __future__ import absolute_import, division, print_function

import copy

import linode_api4

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import filter_null_values

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
---
module: instance
description: Manage Linode instances.
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
      - The unique label to give this instance.
    required: true
    type: string
  type:
    description:
      - The type or plan of this instance.
      - See U(https://api.linode.com/v4/linode/types)
  region:
    description:
      - The location to deploy the instance in.
      - See U(https://api.linode.com/v4/regions)
    required: true
    type: str
  image:
    description:
      - The image ID to deploy the instance disk from.
    required: true
    type: str
  group:
    description:
       - The group that the instance should be marked under. Please note, that
        group labelling is deprecated but still supported. The encouraged
        method for marking instances is to use tags.
    type: str
    required: false
  tags:
    description:
      - The tags that the instance should be marked under.
      - See U(https://www.linode.com/docs/api/tags/).
    required: false
    type: list
  root_pass:
    description:
      - The password for the root user. If not specified, one will be
        generated. This generated password will be available in the task
        success JSON.
    required: false
    type: str
  private_ip:
    description:
      - If true, the created Linode will have private networking enabled.
    required: false
    type: bool
  authorized_keys:
    description:
      - A list of SSH public key parts to deploy for the root user.
    required: false
    type: list
  stackscript_id:
    description:
      - The ID of the StackScript to use when creating the instance.
        See U(https://www.linode.com/docs/api/stackscripts/).
    type: int
    required: false
  stackscript_data:
    description:
      - An object containing arguments to any User Defined Fields present in
        the StackScript used when creating the instance.
        Only valid when a stackscript_id is provided.
        See U(https://www.linode.com/docs/api/stackscripts/).
    type: dict
    required: false
  booted:
    description:
      - Whether the new Instance should be booted. 
        This will default to True if the Instance is deployed from an Image or Backup.
  backup_id:
    description:
      - The id of the Backup to restore to the new Instance. 
        May not be provided if “image” is given.
  state:
    description:
      - The desired instance state.
    type: str
    choices:
      - present
      - absent
'''

EXAMPLES = '''
- name: Create a new Linode instance.
  linode.cloud.instance:
    label: my-linode
    type: g6-nanode-1
    region: us-east
    image: linode/ubuntu20.04
    root_pass: verysecurepassword!!!
    private_ip: false
    authorized_keys:
      - "ssh-rsa ..."
    stackscript_id: 1337
    stackscript_data:
      variable: value
    group: app
    tags:
      - env=prod
    state: present

- name: Delete that new Linode instance.
  linode.cloud.instance:
    label: my-linode
    state: absent
'''

RETURN = '''
instance:
  description: The instance description in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/linode-instances/#linode-view__responses"
  returned: always
  type: dict
  sample: {
    "root_pass": "foobar",  # if auto-generated
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
    "created": "2018-09-26T08:12:33",
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
    "updated": "2018-09-26T10:10:14",
    "watchdog_enabled": true
  }
'''

try:
    from linode_api4 import Instance
except ImportError:
    # handled in module_utils.linode_common
    pass

linode_instance_spec: dict = dict(
    type=dict(type='str'),
    region=dict(type='str'),
    image=dict(type='str'),
    authorized_keys=dict(type='list'),
    root_pass=dict(type='str', no_log=True),
    stackscript_id=dict(type='int'),
    stackscript_data=dict(type='dict'),
    private_ip=dict(type='bool'),
    group=dict(type='str'),
    booted=dict(type='bool'),
    backup_id=dict(type='int')
)

# Fields that can be updated on an existing instance
linode_instance_mutable: set[str] = {
    'group',
    'tags'
}

class LinodeInstance(LinodeModuleBase):
    """Configuration class for a Linode instance resource"""

    def __init__(self):
        self.module_arg_spec = linode_instance_spec

        self.results: dict = dict(
            changed=False,
            actions=[],
            instance=None,
        )

        self._instance: Instance = None
        self._root_pass: str = ''

        super().__init__(module_arg_spec=self.module_arg_spec)

    def get_instance_by_label(self, label) -> Instance:
        """Gets a Linode instance by label"""

        try:
            return self.client.linode.instances(Instance.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get instance {0}: {1}'.format(label, exception))

    def create_instance(self, spec_args: dict) -> dict:
        """Creates a Linode instance"""
        spec_args = copy.deepcopy(spec_args)

        if 'root_pass' in spec_args.keys() and spec_args.get('root_pass') is None:
            spec_args.pop('root_pass')

        ltype = spec_args.pop('type')
        region = spec_args.pop('region')

        result = {
            'instance': None,
            'root_pass': ''
        }

        try:
            response = self.client.linode.instance_create(ltype, region, **spec_args)
        except Exception as exception:
            self.fail(msg='failed to create instance: {0}'.format(exception))

        # Weird variable return type
        if isinstance(response, tuple):
            result['instance'] = response[0]
            result['root_pass'] = response[1]
        else:
            result['instance'] = response

        return result

    def __update_instance(self, spec_args: dict):
        """Update instance handles all update functionality for the current instance"""
        should_update = False

        spec_args = filter_null_values(spec_args)

        for key, new_value in spec_args.items():
            if not hasattr(self._instance, key):
                continue

            old_value = getattr(self._instance, key)

            # Convert type objects to their string IDs
            if type(old_value) in {
                linode_api4.objects.linode.Type,
                linode_api4.objects.linode.Region,
                linode_api4.objects.linode.Image
            }:
                old_value = old_value.id

            if new_value != old_value:
                if key in linode_instance_mutable:
                    setattr(self._instance, key, new_value)
                    self.register_action('Updated instance {0}: "{1}" -> "{2}"'.
                                         format(key, old_value, new_value))

                    should_update = True

                    continue

                self.fail(
                    'failed to update instance {0}: {1} is a non-updatable field'
                    .format(self._instance.label, key))

        if should_update:
            self._instance.save()

    def __handle_instance(self, spec_args: dict):
        """Updates the instance defined in kwargs"""
        label = spec_args.get('label')

        self._instance = self.get_instance_by_label(label)

        if self._instance is None:
            result = self.create_instance(spec_args)
            self._instance = result.get('instance')
            self._root_pass = result.get('root_pass')

            self.register_action('Created instance {0}'.format(label))
        else:
            self.__update_instance(spec_args)

        self._instance._api_get()
        inst_result = self._instance._raw_json
        inst_result['root_pass'] = self._root_pass

        self.results['instance'] = inst_result

    def __handle_instance_absent(self, spec_args: dict):
        """Destroys the instance defined in kwargs"""
        label = spec_args.get('label')

        self._instance = self.get_instance_by_label(label)

        if self._instance is not None:
            self.results['instance'] = self._instance._raw_json
            self.register_action('Deleted instance {0}'.format(label))
            self._instance.delete()

    def exec_module(self, **kwargs) -> dict:
        """Entrypoint for Instance module"""

        state = kwargs.get('state')

        if state == 'absent':
            self.__handle_instance_absent(kwargs)
            return self.results

        self.__handle_instance(kwargs)
        return self.results


def main():
    """Constructs and calls the Linode instance module"""

    LinodeInstance()


if __name__ == '__main__':
    main()
