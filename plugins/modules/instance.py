#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode instances."""

from __future__ import absolute_import, division, print_function

import copy

from typing import Optional, Any, cast, Set, List, Dict, Union
import linode_api4
import polling

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    filter_null_values, paginated_list_to_json, drop_empty_strings, mapping_to_dict

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
description:
- Manage Linode Instances.
module: instance
options:
  authorized_keys:
    description: A list of SSH public key parts to deploy for the root user.
    elements: str
    required: false
    type: list
  backup_id:
    description:
    - The id of the Backup to restore to the new Instance.
    - "May not be provided if \u201Cimage\u201D is given."
    required: false
    type: int
  boot_config_label:
    description: The label of the config to boot from.
    required: false
    type: str
  booted:
    description:
    - Whether the new Instance should be booted.
    - This will default to True if the Instance is deployed from an Image or Backup.
    required: false
    type: bool
  configs:
    description:
    - A list of Instance configs to apply to the Linode.
    - See U(https://www.linode.com/docs/api/linode-instances/#configuration-profile-create)
    elements: dict
    required: false
    suboptions:
      comments:
        description: Arbitrary User comments on this Config.
        required: false
        type: str
      devices:
        description: The devices to map to this configuration.
        required: false
        suboptions:
          sda:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
          sdb:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
          sdc:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
          sdd:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
          sde:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
          sdf:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
          sdg:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
          sdh:
            description: []
            required: false
            suboptions:
              disk_id:
                description: The ID of the disk to attach to this Linode.
                required: false
                type: int
              disk_label:
                description: The label of the disk to attach to this Linode.
                required: false
                type: str
              volume_id:
                description: The ID of the volume to attach to this Linode.
                required: false
                type: int
            type: dict
        type: dict
      helpers:
        description: Helpers enabled when booting to this Linode Config.
        required: false
        suboptions:
          devtmpfs_automount:
            description: Populates the /dev directory early during boot without udev.
            required: false
            type: bool
          distro:
            description: Helps maintain correct inittab/upstart console device.
            required: false
            type: bool
          modules_dep:
            description: Creates a modules dependency file for the Kernel you run.
            required: false
            type: bool
          network:
            description: Automatically configures static networking.
            required: false
            type: bool
          updatedb_disabled:
            description: Disables updatedb cron job to avoid disk thrashing.
            required: false
            type: bool
        type: dict
      kernel:
        description: "A Kernel ID to boot a Linode with. Defaults to \u201Clinode/latest-64bit\u201D\
          ."
        required: false
        type: str
      label:
        description: The label to assign to this config.
        required: true
        type: str
      memory_limit:
        description: Defaults to the total RAM of the Linode.
        required: false
        type: int
      root_device:
        description: The root device to boot.
        required: false
        type: str
      run_level:
        description: Defines the state of your Linode after booting.
        required: false
        type: str
      virt_mode:
        choices:
        - paravirt
        - fullvirt
        description: Controls the virtualization mode.
        required: false
        type: str
    type: list
  disks:
    description:
    - A list of Disks to create on the Linode.
    - See U(https://www.linode.com/docs/api/linode-instances/#disk-create)
    elements: dict
    required: false
    suboptions:
      authorized_keys:
        description: A list of SSH public key parts to deploy for the root user.
        elements: str
        required: false
        type: list
      authorized_users:
        description: A list of usernames.
        elements: str
        required: false
        type: list
      filesystem:
        description: The filesystem to create this disk with.
        required: false
        type: str
      image:
        description: An Image ID to deploy the Disk from.
        required: false
        type: str
      label:
        description: The label to give this Disk.
        required: true
        type: str
      root_pass:
        description: "The root user\u2019s password on the newly-created Linode."
        required: false
        type: str
      size:
        description: The size of the Disk in MB.
        required: true
        type: int
      stackscript_data:
        description:
        - An object containing arguments to any User Defined Fields present in the
          StackScript used when creating the instance.
        - Only valid when a stackscript_id is provided.
        - See U(https://www.linode.com/docs/api/stackscripts/)
        required: false
        type: dict
      stackscript_id:
        description:
        - The ID of the StackScript to use when creating the instance.
        - See U(https://www.linode.com/docs/api/stackscripts/)
        required: false
        type: int
    type: list
  group:
    description:
    - The group that the instance should be marked under.
    - Please note, that group labelling is deprecated but still supported.
    - The encouraged method for marking instances is to use tags.
    required: false
    type: str
  image:
    description: The image ID to deploy the instance disk from.
    required: false
    type: str
  interfaces:
    description:
    - A list of network interfaces to apply to the Linode.
    - See U(https://www.linode.com/docs/api/linode-instances/#linode-create__request-body-schema).
    elements: dict
    required: false
    suboptions:
      ipam_address:
        description: "This Network Interface\u2019s private IP address in Classless\
          \ Inter-Domain Routing (CIDR) notation."
        required: false
        type: str
      label:
        description:
        - The name of this interface.
        - Required for vlan purpose interfaces.
        - Must be an empty string or null for public purpose interfaces.
        required: false
        type: str
      purpose:
        choices:
        - public
        - vlan
        description: The type of interface.
        required: true
        type: str
    type: list
  private_ip:
    description: If true, the created Linode will have private networking enabled.
    required: false
    type: bool
  region:
    description:
    - The location to deploy the instance in.
    - See U(https://api.linode.com/v4/regions)
    required: false
    type: str
  root_pass:
    description:
    - The password for the root user.
    - If not specified, one will be generated.
    - This generated password will be available in the task success JSON.
    required: false
    type: str
  stackscript_data:
    description:
    - An object containing arguments to any User Defined Fields present in the StackScript
      used when creating the instance.
    - Only valid when a stackscript_id is provided.
    - See U(https://www.linode.com/docs/api/stackscripts/).
    required: false
    type: dict
  stackscript_id:
    description:
    - The ID of the StackScript to use when creating the instance.
    - See U(https://www.linode.com/docs/api/stackscripts/).
    required: false
    type: int
  type:
    description:
    - The unique label to give this instance.
    required: false
    type: str
  wait:
    default: true
    description: Wait for the instance to have status `running` before returning.
    required: false
    type: bool
  wait_timeout:
    default: 240
    description: The amount of time, in seconds, to wait for an instance to have status
      `running`.
    required: false
    type: int
requirements:
- python >= 3.0
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

try:
    from linode_api4 import Instance, Config, ConfigInterface, Disk, Volume
except ImportError:
    # handled in module_utils.linode_common
    pass

linode_instance_disk_spec = dict(
    authorized_keys=dict(
        type='list', elements='str',
        description='A list of SSH public key parts to deploy for the root user.'),

    authorized_users=dict(
        type='list', elements='str',
        description='A list of usernames.'),

    filesystem=dict(
        type='str',
        description='The filesystem to create this disk with.'),

    image=dict(
        type='str',
        description='An Image ID to deploy the Disk from.'),

    label=dict(
        type='str', required=True,
        description='The label to give this Disk.'),

    root_pass=dict(
        type='str',
        description='The root user’s password on the newly-created Linode.'),

    size=dict(
        type='int', required=True,
        description='The size of the Disk in MB.'),

    stackscript_id=dict(
        type='int',
        description=[
            'The ID of the StackScript to use when creating the instance.',
            'See U(https://www.linode.com/docs/api/stackscripts/)'
        ]),

    stackscript_data=dict(
        type='dict',
        description=[
            'An object containing arguments to any User Defined Fields present in '
            'the StackScript used when creating the instance.',
            'Only valid when a stackscript_id is provided.',
            'See U(https://www.linode.com/docs/api/stackscripts/)'
        ])
)

linode_instance_device_spec = dict(
    disk_label=dict(
        type='str',
        description='The label of the disk to attach to this Linode.'),

    disk_id=dict(
        type='int',
        description='The ID of the disk to attach to this Linode.'),

    volume_id=dict(
        type='int',
        description='The ID of the volume to attach to this Linode.')
)

linode_instance_devices_spec = dict(
    sda=dict(type='dict', options=linode_instance_device_spec),
    sdb=dict(type='dict', options=linode_instance_device_spec),
    sdc=dict(type='dict', options=linode_instance_device_spec),
    sdd=dict(type='dict', options=linode_instance_device_spec),
    sde=dict(type='dict', options=linode_instance_device_spec),
    sdf=dict(type='dict', options=linode_instance_device_spec),
    sdg=dict(type='dict', options=linode_instance_device_spec),
    sdh=dict(type='dict', options=linode_instance_device_spec),
)

linode_instance_helpers_spec = dict(
    devtmpfs_automount=dict(
        type='bool',
        description='Populates the /dev directory early during boot without udev.'),

    distro=dict(
        type='bool',
        description='Helps maintain correct inittab/upstart console device.'),

    modules_dep=dict(
        type='bool',
        description='Creates a modules dependency file for the Kernel you run.'),

    network=dict(
        type='bool',
        description='Automatically configures static networking.'),

    updatedb_disabled=dict(
        type='bool',
        description='Disables updatedb cron job to avoid disk thrashing.')
)

linode_instance_interface_spec = dict(
    purpose=dict(
        type='str', required=True,
        description='The type of interface.',
        choices=[
            'public',
            'vlan'
        ]),

    label=dict(
        type='str',
        description=[
            'The name of this interface.',
            'Required for vlan purpose interfaces.',
            'Must be an empty string or null for public purpose interfaces.'
        ]),

    ipam_address=dict(
        type='str',
        description='This Network Interface’s private IP address in Classless '
                    'Inter-Domain Routing (CIDR) notation.'
    )
)

linode_instance_config_spec = dict(
    comments=dict(
        type='str',
        description='Arbitrary User comments on this Config.'),

    devices=dict(
        type='dict', options=linode_instance_devices_spec,
        description='The devices to map to this configuration.'),

    helpers=dict(
        type='dict', options=linode_instance_helpers_spec,
        description='Helpers enabled when booting to this Linode Config.'),

    kernel=dict(
        type='str',
        description='A Kernel ID to boot a Linode with. Defaults to “linode/latest-64bit”.'),

    label=dict(
        type='str', required=True,
        description='The label to assign to this config.'),

    memory_limit=dict(
        type='int',
        description='Defaults to the total RAM of the Linode.'),

    root_device=dict(
        type='str',
        description='The root device to boot.'),

    run_level=dict(
        type='str',
        description='Defines the state of your Linode after booting.'),

    virt_mode=dict(
        type='str',
        description='Controls the virtualization mode.',
        choices=[
            'paravirt',
            'fullvirt'
        ])
)

linode_instance_spec = dict(
    type=dict(type='str', description=['The unique label to give this instance.']),
    region=dict(
        type='str',
        description=[
            'The location to deploy the instance in.',
            'See U(https://api.linode.com/v4/regions)']),

    image=dict(
        type='str',
        description='The image ID to deploy the instance disk from.'),

    authorized_keys=dict(
        type='list', elements='str',
        description='A list of SSH public key parts to deploy for the root user.'),

    root_pass=dict(
        type='str', no_log=True,
        description=[
            'The password for the root user.',
            'If not specified, one will be generated.',
            'This generated password will be available in the task success JSON.'
        ]),

    stackscript_id=dict(
        type='int',
        description=[
            'The ID of the StackScript to use when creating the instance.',
            'See U(https://www.linode.com/docs/api/stackscripts/).'
        ]),

    stackscript_data=dict(
        type='dict',
        description=[
            'An object containing arguments to any User Defined Fields present in '
            'the StackScript used when creating the instance.',
            'Only valid when a stackscript_id is provided.',
            'See U(https://www.linode.com/docs/api/stackscripts/).'
        ]),

    private_ip=dict(
        type='bool',
        description='If true, the created Linode will have private networking enabled.'),

    group=dict(
        type='str',
        description=[
            'The group that the instance should be marked under.',
            'Please note, that group labelling is deprecated but still supported.',
            'The encouraged method for marking instances is to use tags.']),

    boot_config_label=dict(type='str', description='The label of the config to boot from.'),

    configs=dict(
        type='list', elements='dict', options=linode_instance_config_spec,
        description=[
            'A list of Instance configs to apply to the Linode.',
            'See U(https://www.linode.com/docs/api/linode-instances/#configuration-profile-create)'
        ]),

    disks=dict(
        type='list', elements='dict', options=linode_instance_disk_spec,
        description=[
            'A list of Disks to create on the Linode.',
            'See U(https://www.linode.com/docs/api/linode-instances/#disk-create)'
        ]),

    interfaces=dict(
        type='list', elements='dict', options=linode_instance_interface_spec,
        description=[
            'A list of network interfaces to apply to the Linode.',
            'See U(https://www.linode.com/docs/api/linode-instances/'
            '#linode-create__request-body-schema).'
        ]),

    booted=dict(
        type='bool',
        description=[
            'Whether the new Instance should be booted.',
            'This will default to True if the Instance is deployed from an Image or Backup.'
        ]),

    backup_id=dict(
        type='int',
        description=[
            'The id of the Backup to restore to the new Instance.',
            'May not be provided if “image” is given.']),

    wait=dict(
        type='bool', default=True,
        description='Wait for the instance to have status `running` before returning.'),

    wait_timeout=dict(
        type='int', default=240,
        description='The amount of time, in seconds, to wait for an instance to '
                    'have status `running`.'
        )
)

specdoc_meta = dict(
    description=[
        'Manage Linode Instances.'
    ],
    requirements=[
        'python >= 3.0'
    ],
    author=[
        'Luke Murphy (@decentral1se)',
        'Charles Kenney (@charliekenney23)',
        'Phillip Campbell (@phillc)',
        'Lena Garber (@lbgarber)'
    ],
    spec=linode_instance_spec
)

# Fields that can be updated on an existing instance
linode_instance_mutable = {
    'group',
    'tags'
}

linode_instance_config_mutable = {
    'comments',
    'kernel',
    'memory_limit',
    'root_device',
    'run_level',
    'virt_mode'
}


class LinodeInstance(LinodeModuleBase):
    """Module for creating and destroying Linode Instances"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_instance_spec

        self.mutually_exclusive = [
            ('image', 'disks'),
            ('image', 'configs'),
        ]

        self.results: dict = dict(
            changed=False,
            actions=[],
            instance=None,
            configs=None,
        )

        self._instance: Optional[Instance] = None
        self._root_pass: str = ''

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            mutually_exclusive=self.mutually_exclusive)

    def _get_instance_by_label(self, label: str) -> Optional[Instance]:
        """Gets a Linode instance by label"""

        try:
            return self.client.linode.instances(Instance.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get instance {0}: {1}'.format(label, exception))

    def _get_desired_instance_status(self) -> str:
        booted = self.module.params.get('booted')
        disks = self.module.params.get('disks')
        configs = self.module.params.get('configs')

        if not booted or \
                (disks is not None and len(disks) > 0) or \
                (configs is not None and len(configs) > 0):
            return 'offline'

        return 'running'

    def _get_boot_config(self) -> Optional[Config]:
        config_label = self.module.params.get('boot_config_label')

        if config_label is not None:
            # Find the config with the matching label
            return next(
                (config for config in self._instance.configs if config.label == config_label),
                None)

        if len(self._instance.configs) > 0:
            return self._instance.configs[0]

        return None

    def _get_disk_by_label(self, label: str) -> Optional[Disk]:
        # Find the disk with the matching label
        return next((disk for disk in self._instance.disks if disk.label == label), None)

    @staticmethod
    def _device_to_param_mapping(device: Union[Disk, Volume]) -> Dict[str, int]:
        id_key = ''

        if isinstance(device, Volume):
            id_key = 'volume_id'

        if isinstance(device, Disk):
            id_key = 'disk_id'

        return {
            id_key: device.id
        }

    def _compare_param_to_device(
            self, device_param: Dict[str, Any], device: Union[Disk, Volume]) -> bool:
        if device is None or device_param is None:
            return device == device_param

        device_mapping = self._device_to_param_mapping(device)

        disk_label = device_param.get('disk_label')
        if disk_label is not None:
            disk = self._get_disk_by_label(disk_label)
            if disk is None:
                self.fail('invalid disk specified')

            device_param = {
                'disk_id': disk.id
            }

        return filter_null_values(device_mapping) == filter_null_values(device_param)

    def _create_instance(self) -> dict:
        """Creates a Linode instance"""
        params = copy.deepcopy(self.module.params)

        if 'root_pass' in params.keys() and params.get('root_pass') is None:
            params.pop('root_pass')

        ltype = params.pop('type')
        region = params.pop('region')

        result = {
            'instance': None,
            'root_pass': ''
        }

        try:
            response = self.client.linode.instance_create(ltype, region, **params)

        except Exception as exception:
            self.fail(msg='failed to create instance: {0}'.format(exception))

        # Weird variable return type
        if isinstance(response, tuple):
            result['instance'] = response[0]
            result['root_pass'] = response[1]
        else:
            result['instance'] = response

        return result

    def _param_device_to_device(self, device: Dict[str, Any]) -> Union[Disk, Volume, None]:
        if device is None:
            return None

        disk_label = device.get('disk_label')
        disk_id = device.get('disk_id')
        volume_id = device.get('volume_id')

        if disk_label is not None:
            disk = self._get_disk_by_label(disk_label)
            if disk is None:
                self.fail('invalid disk label: {0}'.format(disk_label))

            return disk

        if disk_id is not None:
            return Disk(self.client, device.get('disk_id'), self._instance.id)

        if volume_id is not None:
            return Volume(self.client, device.get('volume_id'))

        return None

    def _create_config_register(self, config_params: Dict[str, Any]) -> None:
        device_params = config_params.pop('devices')
        devices = []

        for device_suffix in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            device_dict = device_params.get('sd{0}'.format(device_suffix))
            devices.append(self._param_device_to_device(device_dict))

        self._instance.config_create(devices=devices, **filter_null_values(config_params))
        self.register_action('Created config {0}'.format(config_params.get('label')))

    def _delete_config_register(self, config: Config) -> None:
        self.register_action('Deleted config {0}'.format(config.label))
        config.delete()

    def _create_disk_register(self, **kwargs: Any) -> None:
        size = kwargs.pop('size')
        result = self._instance.disk_create(size, **kwargs)

        if isinstance(result, tuple):
            disk = result[0]
        else:
            disk = result

        # The disk must be ready before the next disk is created
        self._wait_for_disk_status(disk, {'ready'}, self.module.params.get('wait_timeout'))

        self.register_action('Created disk {0}'.format(kwargs.get('label')))

    def _delete_disk_register(self, disk: Disk) -> None:
        self.register_action('Deleted disk {0}'.format(disk.label))
        disk.delete()

    def _wait_for_instance_status(self, instance: Instance, status: Set[str], timeout: int,
                                  not_status: bool = False) -> None:
        def poll_func() -> bool:
            return (instance.status in status) != not_status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=10,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail('failed to wait for instance: timeout period expired')

    def _wait_for_disk_status(
            self, disk: Disk, status: Set[str], timeout: int, not_status: bool = False) \
            -> None:
        try:
            polling.poll(
                lambda: (disk.status in status) != not_status,
                step=10,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail('failed to wait for disk: timeout period expired')

    def _update_interfaces(self) -> None:
        config = self._get_boot_config()
        param_interfaces: List[Any] = self.module.params.get('interfaces')

        if config is None or param_interfaces is None:
            return

        param_interfaces = [drop_empty_strings(v) for v in param_interfaces]
        remote_interfaces = [drop_empty_strings(v._serialize()) for v in config.interfaces]

        if remote_interfaces == param_interfaces:
            return

        config.interfaces = [ConfigInterface(**v) for v in param_interfaces]
        config.save()

        self.register_action('Updated interfaces for instance {0} config {1}'
                             .format(self._instance.label, config.id))

    def _update_config(self, config: Config, config_params: Dict[str, Any]) -> None:
        should_update = False
        params = filter_null_values(config_params)

        for key, new_value in params.items():
            if not hasattr(config, key):
                continue

            old_value = mapping_to_dict(getattr(config, key))

            # Special diffing due to handling in linode_api4-python
            if key == 'devices':
                for device_key, device in old_value.items():
                    if not self._compare_param_to_device(new_value[device_key], device):
                        self.fail('failed to update config: {0} is a non-mutable field'
                                  .format('devices'))

                continue

            if new_value != old_value:
                if key in linode_instance_config_mutable:
                    setattr(config, key, new_value)
                    self.register_action('Updated Config {0}: "{1}" -> "{2}"'.
                                         format(key, old_value, new_value))
                    should_update = True
                    continue

                self.fail('failed to update config: {0} is a non-mutable field'.format(key))

        if should_update:
            config.save()

    def _update_configs(self) -> None:
        current_configs = self._instance.configs

        if self.module.params.get('image') is not None:
            return

        config_params = self.module.params['configs'] or []
        config_map: Dict[str, Config] = {}

        for config in current_configs:
            config_map[config.label] = config

        for config in config_params:
            config_label = config['label']

            if config_label in config_map:
                self._update_config(config_map[config_label], config)

                del config_map[config_label]
                continue

            self._create_config_register(config)

        for config in config_map.values():
            self._delete_config_register(config)

    def _update_disk(self, disk: Disk, disk_params: Dict[str, Any]) -> None:
        new_size = disk_params.pop('size')

        if disk.size != new_size:
            disk.resize(new_size)
            self.register_action('Resized disk {0}: {1} -> {2}'
                                 .format(disk.label, disk.size, new_size))
            disk._api_get()
            self._wait_for_disk_status(disk, {'ready'}, self.module.params.get('wait_timeout'))

        for key, new_value in filter_null_values(disk_params).items():
            if not hasattr(disk, key):
                continue

            old_value = getattr(disk, key)
            if new_value != old_value:
                self.fail('failed to update disk: {0} is a non-mutable field'.format(key))

    def _update_disks(self) -> None:
        current_disks = self._instance.disks

        # Instances with implicit disks should be ignored
        if self.module.params.get('image') is not None:
            return

        disk_params = self.module.params['disks'] or []

        disk_map: Dict[str, Disk] = {}

        for disk in current_disks:
            disk_map[disk.label] = disk

        for disk in disk_params:
            disk_label = disk['label']

            if disk_label in disk_map:
                self._update_disk(disk_map[disk_label], disk)

                del disk_map[disk_label]
                continue

            self._create_disk_register(**disk)

        if len(disk_map.values()) > 0:
            self.fail('unable to update disks: disks must be removed manually')

    def _update_instance(self) -> None:
        """Update instance handles all update functionality for the current instance"""
        should_update = False

        params = filter_null_values(self.module.params)

        for key, new_value in params.items():
            if not hasattr(self._instance, key):
                continue

            if key in {'configs', 'disks', 'boot_config_label'}:
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

        # Update interfaces
        self._update_interfaces()

    def _handle_instance_boot(self) -> None:
        boot_status = self.module.params.get('booted')
        should_poll = self.module.params.get('wait')

        # Wait for instance to not be busy
        self._wait_for_instance_status(
            self._instance,
            {'running', 'offline'},
            self.module.params.get('wait_timeout'))

        self._instance._api_get()

        desired_status = None

        if boot_status and self._instance.status != 'running':
            self._instance.boot(self._get_boot_config())
            self.register_action('Booted instance {0}'.format(self.module.params.get('label')))
            desired_status = {'running'}

        if not boot_status and self._instance.status != 'offline':
            self._instance.shutdown()
            self.register_action('Shutdown instance {0}'.format(self.module.params.get('label')))
            desired_status = {'offline'}

        if should_poll and desired_status is not None:
            self._wait_for_instance_status(
                self._instance,
                desired_status,
                self.module.params.get('wait_timeout'))

    def _handle_present(self) -> None:
        """Updates the instance defined in kwargs"""

        label = self.module.params.get('label')

        self._instance = self._get_instance_by_label(label)

        if self._instance is None:
            result = self._create_instance()
            self._instance = cast(Instance, result.get('instance'))
            self._root_pass = str(result.get('root_pass'))

            self.register_action('Created instance {0}'.format(label))
        else:
            self._update_instance()

        # Wait for Linode to not be busy if configs or disks need to be created
        # This eliminates the need for unnecessary polling
        disks = self.module.params.get('disks') or []
        configs = self.module.params.get('configs') or []

        if len(configs) > 0 or len(disks) > 0:
            self._wait_for_instance_status(
                self._instance,
                {'offline', 'running'},
                self.module.params.get('wait_timeout'))

            self._update_disks()
            self._update_configs()

        if self.module.params.get('booted') is not None:
            self._handle_instance_boot()

        self._instance._api_get()
        inst_result = self._instance._raw_json
        inst_result['root_pass'] = self._root_pass

        self.results['instance'] = inst_result
        self.results['configs'] = paginated_list_to_json(self._instance.configs)
        self.results['disks'] = paginated_list_to_json(self._instance.disks)

    def _handle_absent(self) -> None:
        """Destroys the instance defined in kwargs"""
        label = self.module.params.get('label')

        self._instance = self._get_instance_by_label(label)

        if self._instance is not None:
            self.results['instance'] = self._instance._raw_json
            self.results['configs'] = paginated_list_to_json(self._instance.configs)
            self.results['disks'] = paginated_list_to_json(self._instance.disks)
            self.register_action('Deleted instance {0}'.format(label))
            self._instance.delete()

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Instance module"""

        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode instance module"""

    LinodeInstance()


if __name__ == '__main__':
    main()
