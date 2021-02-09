#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: instance
description: Manage Linode instances.
requirements:
  - python: >= 2.7
  - linode_api4: >= 3.0
author:
  - Luke Murphy (@decentral1se)
  - Charles Kenney (@charliekenney23)
  - Phillip Campbell (@phillc)
options:
  label:
    desription:
      - The unique label to give this instance.
    required: true
    type: string
  type:
    description:
      - The type or plan of this instance.
      - See: U(https://api.linode.com/v4/linode/types)
  region:
    description:
      - The location to deploy the instance in.
      - See: U(https://api.linode.com/v4/regions)
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
      - The tags that the instance should be marked under. See
        U(https://www.linode.com/docs/api/tags/).
    required: false
    type: list
  root_pass:
    description:
      - The password for the root user. If not specified, one will be
        generated. This generated password will be available in the task
        success JSON.
    required: false
    type: str
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
  returned: Always.
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
    "id": 10480444,
    "image": "linode/ubuntu20.04",
    "ipv4": [
      "130.132.285.233"
    ],
    "ipv6": "2a82:7e00::h03c:46ff:fe04:5cd2/64",
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

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

try:
  from linode_api4 import Instance
except ImportError:
  # handled in module_utils.linode_common
  pass


class LinodeInstance(LinodeModuleBase):
  """Configuration class for a Linode instance resource"""

  def __init__(self):

    self.module_arg_spec = dict(
      type=dict(type='str', required=False),
      region=dict(type='str', required=False),
      image=dict(type='str', required=False),
      authorized_key=dict(type='list', required=False),
      group=dict(type='str', required=False),
      root_pass=dict(type='str', required=False, no_log=True),
      stackscript_id=dict(type='int', required=False),
      stackscript_data=dict(type='dict', required=False)
    )

    self.required_one_of=['state', 'label']
    self.required_together=['region', 'image', 'type']

    self.results = dict(
      changed=False,
      actions=[],
      instance=None,
    )

    self.results = dict(
      changed=False,
      actions=[],
      instance=None,
    )

    super(LinodeInstance, self).__init__(module_arg_spec=self.module_arg_spec,
      required_one_of=self.required_one_of, required_together=self.required_together)


  def get_instance_by_label(self, label):
    """Gets a Linode instance by label"""

    try:
      res = self.client.linode.instances(Instance.label == label)
      return res[0]
    except IndexError:
      return None
    except Exception as exception:
      self.fail(msg='failed to get instance {0}: {1}'.format(label, exception))


  def create_linode(self, **kwargs):
    """Creates a Linode instance"""

    if kwargs['root_pass'] is None:
      kwargs.pop('root_pass')

    try:
      res = self.client.linode.instance_create(**kwargs)
    except Exception as exception:
      self.fail(msg='failed to create instance: {0}'.format(exception))

    try:
      if isinstance(res, tuple):
        instance, root_pass = res
        instance_json = instance._raw_json
        instance_json.update({'root_pass': root_pass})
        return instance_json
      else:
        return res._raw_json
    except TypeError:
      self.fail(msg='unable to parse Linode instance creation response')


  def exec_module(self, **kwargs):
    label = kwargs.get('label')
    state = kwargs.get('state')
    instance = self.get_instance_by_label(label)

    if state == 'present' and instance is not None:
      return dict(changed=False, instance=instance._raw_json)

    elif state == 'present' and instance is None:
      instance_json = self.create_linode(
        label=label,
        authorized_keys=kwargs.get('authorized_keys'),
        group=kwargs.get('group'),
        image=kwargs.get('image'),
        region=kwargs.get('region'),
        root_pass=kwargs.get('root_pass'),
        tags=kwargs.get('tags'),
        ltype=kwargs.get('type'),
        stackscript=kwargs.get('stackscript_id'),
        stackscript_data=kwargs.get('stackscript_data'),
      )
      return dict(changed=True, instance=instance_json)

    elif state == 'absent' and instance is not None:
      instance.delete()
      return dict(changed=True, instance=instance._raw_json)

    return dict(changed=False, instance={})


def main():
  LinodeInstance()


if __name__ == '__main__':
  main()
