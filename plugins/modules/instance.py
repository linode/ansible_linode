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
  configs:
    description:
      - A list of Instance configs to apply to the Linode.
      - See U(https://www.linode.com/docs/api/linode-instances/#configuration-profile-create)
    type: list
    elements: dict
    suboptions:
      label:
        description:
          - The label to assign to this config.
        type: str
        required: true
      comments:
        description:
          - Arbitrary User comments on this Config.
        type: str
      devices:
        description:
          - A map of devices to use in a Linode's configuration profile.
        type: list
        elements: dict
        suboptions:
          sda...sdh:
            description:
              - A device to be mapped to to this configuration.
            type: dict
            suboptions:
              disk_label:
                description:
                  - The label of the disk to attach to this Linode.
                type: str
              disk_id:
                description:
                  - The ID of the disk to attach to this Linode.
                type: int
              volume_id:
                description:
                  - The ID of the volume to attach to this Linode.
                type: int
      helpers:
        description:
          - Helpers enabled when booting to this Linode Config.
        type: dict
        suboptions:
          devtmpfs_automount:
            description:
              - Populates the /dev directory early during boot without udev.
            type: bool
          distro:
            description:
              - Helps maintain correct inittab/upstart console device.
            type: bool
          modules_dep:
            description:
              - Creates a modules dependency file for the Kernel you run.
            type: bool
          network:
            description:
              - Automatically configures static networking.
            type: bool
          updatedb_disabled:
            description:
              - Disables updatedb cron job to avoid disk thrashing.
            type: bool
      kernel:
        description:
          - A Kernel ID to boot a Linode with. Defaults to “linode/latest-64bit”.
        type: str
      memory_limit:
        description:
          - Defaults to the total RAM of the Linode.
        type: int
      root_device:
        description:
          - The root device to boot.
        type: int
      run_level:
        description:
          - Defines the state of your Linode after booting.
        type: str
        choices:
          - default
          - single
          - binbash
      virt_mode:
        description:
          - Controls the virtualization mode.
        type: str
        choices:
          - paravirt
          - fullvirt
          
  disks:
    description:
      - A list of Disks to create on the Linode.
      - See U(https://www.linode.com/docs/api/linode-instances/#disk-create)
    type: list
    elements: dict
    suboptions:
      label:
        description:
          - The label to give this Disk.
        type: str
        required: true
      size:
        description:
          - The size of the Disk in MB.
        type: int
      authorized_keys:
        description:
          - A list of SSH public key parts to deploy for the root user.
        type: list
        elements: str
      authorized_users:
        description:
          - A list of usernames.
        type: list
        elements: str
      filesystem:
        description:
          - The filesystem to create this disk with.
        type: str
      image:
        description:
          - An Image ID to deploy the Disk from.
        type: str
      root_pass:
        description:
          - The root user’s password on the newly-created Linode.
        type: str
      stackscript_data:
        description:
          - An object containing arguments to any User Defined Fields present in
            the StackScript used when creating the instance.
            Only valid when a stackscript_id is provided.
          - See U(https://www.linode.com/docs/api/stackscripts/).
        type: dict
      stackscript_id:
        description:
          - The ID of the StackScript to use when creating the instance. 
          - See U(https://www.linode.com/docs/api/stackscripts/)
        
  interfaces:
    description:
      - A list of network interfaces to apply to the Linode.
      - VLANs are currently in beta and will only function correctly if `api_version` is set to `v4beta`.
      - See U(https://www.linode.com/docs/api/linode-instances/#linode-create__request-body-schema).
    type: list
    elements: dict
    suboptions:
      purpose:
        description: 
          - The type of interface.
        choices:
          - public
          - vlan
        type: str
        required: true
      label:
        description:
          - The name of this interface.
          - Required for vlan purpose interfaces. 
          - Must be an empty string or null for public purpose interfaces.
        type: str
      ipam_address:
        description:
          - This Network Interface’s private IP address in Classless Inter-Domain Routing (CIDR) notation.
        type: str
  booted:
    description:
      - Whether the new Instance should be booted. 
        This will default to True if the Instance is deployed from an Image or Backup.
  backup_id:
    description:
      - The id of the Backup to restore to the new Instance. 
        May not be provided if “image” is given.
  wait:
    description:
      - Wait for the instance to have status `running` before returning.
    default: True
    type: bool
  wait_timeout:
    description:
      - The amount of time, in seconds, to wait for an instance to have status `running`.
    default: 240
    type: int
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
    authorized_keys=dict(type='list', elements='str'),
    authorized_users=dict(type='list', elements='str'),
    filesystem=dict(type='str'),
    image=dict(type='str'),
    label=dict(type='str', required=True),
    root_pass=dict(type='str'),
    size=dict(type='int', required=True),
    stackscript_id=dict(type='int'),
    stackscript_data=dict(type='dict')
)

linode_instance_device_spec = dict(
    disk_label=dict(type='str'),
    disk_id=dict(type='int'),
    volume_id=dict(type='int')
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
    devtmpfs_automount=dict(type='bool'),
    distro=dict(type='bool'),
    modules_dep=dict(type='bool'),
    network=dict(type='bool'),
    updatedb_disabled=dict(type='bool')
)

linode_instance_interface_spec = dict(
    purpose=dict(type='str', required=True),
    label=dict(type='str'),
    ipam_address=dict(type='str')
)

linode_instance_config_spec = dict(
    comments=dict(type='str'),
    devices=dict(type='dict', options=linode_instance_devices_spec),
    helpers=dict(type='dict', options=linode_instance_helpers_spec),
    kernel=dict(type='str'),
    label=dict(type='str', required=True),
    memory_limit=dict(type='int'),
    root_device=dict(type='str'),
    run_level=dict(type='str'),
    virt_mode=dict(type='str')
)

linode_instance_spec = dict(
    type=dict(type='str'),
    region=dict(type='str'),
    image=dict(type='str'),
    authorized_keys=dict(type='list', elements='str'),
    root_pass=dict(type='str', no_log=True),
    stackscript_id=dict(type='int'),
    stackscript_data=dict(type='dict'),
    private_ip=dict(type='bool'),
    group=dict(type='str'),
    boot_config_label=dict(type='str'),
    configs=dict(type='list', elements='dict', options=linode_instance_config_spec),
    disks=dict(type='list', elements='dict', options=linode_instance_disk_spec),
    interfaces=dict(type='list', elements='dict', options=linode_instance_interface_spec),
    booted=dict(type='bool'),
    backup_id=dict(type='int'),
    wait=dict(type='bool', default=True),
    wait_timeout=dict(type='int', default=240)
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

    def __get_instance_by_label(self, label: str) -> Optional[Instance]:
        """Gets a Linode instance by label"""

        try:
            return self.client.linode.instances(Instance.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get instance {0}: {1}'.format(label, exception))

    def __get_desired_instance_status(self) -> str:
        booted = self.module.params.get('booted')
        disks = self.module.params.get('disks')
        configs = self.module.params.get('configs')

        if not booted or \
                (disks is not None and len(disks) > 0) or \
                (configs is not None and len(configs) > 0):
            return 'offline'

        return 'running'

    def __get_boot_config(self) -> Optional[Config]:
        config_label = self.module.params.get('boot_config_label')

        if config_label is not None:
            # Find the config with the matching label
            return next(
                (config for config in self._instance.configs if config.label == config_label),
                None)

        if len(self._instance.configs) > 0:
            return self._instance.configs[0]

        return None

    def __get_disk_by_label(self, label: str) -> Optional[Disk]:
        # Find the disk with the matching label
        return next((disk for disk in self._instance.disks if disk.label == label), None)

    @staticmethod
    def __device_to_param_mapping(device: Union[Disk, Volume]) -> Dict[str, int]:
        id_key = ''

        if isinstance(device, Volume):
            id_key = 'volume_id'

        if isinstance(device, Disk):
            id_key = 'disk_id'

        return {
            id_key: device.id
        }

    def __compare_param_to_device(
            self, device_param: Dict[str, Any], device: Union[Disk, Volume]) -> bool:
        if device is None or device_param is None:
            return device == device_param

        device_mapping = self.__device_to_param_mapping(device)

        disk_label = device_param.get('disk_label')
        if disk_label is not None:
            disk = self.__get_disk_by_label(disk_label)
            if disk is None:
                self.fail('invalid disk specified')

            device_param = {
                'disk_id': disk.id
            }

        return filter_null_values(device_mapping) == filter_null_values(device_param)

    def __create_instance(self) -> dict:
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

    def __param_device_to_device(self, device: Dict[str, Any]) -> Union[Disk, Volume, None]:
        if device is None:
            return None

        disk_label = device.get('disk_label')
        disk_id = device.get('disk_id')
        volume_id = device.get('volume_id')

        if disk_label is not None:
            disk = self.__get_disk_by_label(disk_label)
            if disk is None:
                self.fail('invalid disk label: {0}'.format(disk_label))

            return disk

        if disk_id is not None:
            return Disk(self.client, device.get('disk_id'), self._instance.id)

        if volume_id is not None:
            return Volume(self.client, device.get('volume_id'))

        return None

    def __create_config_register(self, config_params: Dict[str, Any]) -> None:
        device_params = config_params.pop('devices')
        devices = []

        for device_suffix in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            device_dict = device_params.get('sd{0}'.format(device_suffix))
            devices.append(self.__param_device_to_device(device_dict))

        self._instance.config_create(devices=devices, **filter_null_values(config_params))
        self.register_action('Created config {0}'.format(config_params.get('label')))

    def __delete_config_register(self, config: Config) -> None:
        self.register_action('Deleted config {0}'.format(config.label))
        config.delete()

    def __create_disk_register(self, **kwargs: Any) -> None:
        size = kwargs.pop('size')
        result = self._instance.disk_create(size, **kwargs)

        if isinstance(result, tuple):
            disk = result[0]
        else:
            disk = result

        # The disk must be ready before the next disk is created
        self.__wait_for_disk_status(disk, {'ready'}, self.module.params.get('wait_timeout'))

        self.register_action('Created disk {0}'.format(kwargs.get('label')))

    def __delete_disk_register(self, disk: Disk) -> None:
        self.register_action('Deleted disk {0}'.format(disk.label))
        disk.delete()

    def __wait_for_instance_status(self, instance: Instance, status: Set[str], timeout: int,
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

    def __wait_for_disk_status(
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

    def __update_interfaces(self) -> None:
        config = self.__get_boot_config()
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

    def __update_config(self, config: Config, config_params: Dict[str, Any]) -> None:
        should_update = False
        params = filter_null_values(config_params)

        for key, new_value in params.items():
            if not hasattr(config, key):
                continue

            old_value = mapping_to_dict(getattr(config, key))

            # Special diffing due to handling in linode_api4-python
            if key == 'devices':
                for device_key, device in old_value.items():
                    if not self.__compare_param_to_device(new_value[device_key], device):
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

    def __update_configs(self) -> None:
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
                self.__update_config(config_map[config_label], config)

                del config_map[config_label]
                continue

            self.__create_config_register(config)

        for config in config_map.values():
            self.__delete_config_register(config)

    def __update_disk(self, disk: Disk, disk_params: Dict[str, Any]) -> None:
        new_size = disk_params.pop('size')

        if disk.size != new_size:
            disk.resize(new_size)
            self.register_action('Resized disk {0}: {1} -> {2}'
                                 .format(disk.label, disk.size, new_size))
            disk._api_get()
            self.__wait_for_disk_status(disk, {'ready'}, self.module.params.get('wait_timeout'))

        for key, new_value in filter_null_values(disk_params).items():
            if not hasattr(disk, key):
                continue

            old_value = getattr(disk, key)
            if new_value != old_value:
                self.fail('failed to update disk: {0} is a non-mutable field'.format(key))

    def __update_disks(self) -> None:
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
                self.__update_disk(disk_map[disk_label], disk)

                del disk_map[disk_label]
                continue

            self.__create_disk_register(**disk)

        if len(disk_map.values()) > 0:
            self.fail('unable to update disks: disks must be removed manually')

    def __update_instance(self) -> None:
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
        self.__update_interfaces()

    def __handle_instance_boot(self) -> None:
        boot_status = self.module.params.get('booted')
        should_poll = self.module.params.get('wait')

        # Wait for instance to not be busy
        self.__wait_for_instance_status(
            self._instance,
            {'running', 'offline'},
            self.module.params.get('wait_timeout'))

        self._instance._api_get()

        desired_status = None

        if boot_status and self._instance.status != 'running':
            self._instance.boot(self.__get_boot_config())
            self.register_action('Booted instance {0}'.format(self.module.params.get('label')))
            desired_status = {'running'}

        if not boot_status and self._instance.status != 'offline':
            self._instance.shutdown()
            self.register_action('Shutdown instance {0}'.format(self.module.params.get('label')))
            desired_status = {'offline'}

        if should_poll and desired_status is not None:
            self.__wait_for_instance_status(
                self._instance,
                desired_status,
                self.module.params.get('wait_timeout'))

    def __handle_present(self) -> None:
        """Updates the instance defined in kwargs"""

        label = self.module.params.get('label')

        self._instance = self.__get_instance_by_label(label)

        if self._instance is None:
            result = self.__create_instance()
            self._instance = cast(Instance, result.get('instance'))
            self._root_pass = str(result.get('root_pass'))

            self.register_action('Created instance {0}'.format(label))
        else:
            self.__update_instance()

        # Wait for Linode to not be busy if configs or disks need to be created
        # This eliminates the need for unnecessary polling
        disks = self.module.params.get('disks') or []
        configs = self.module.params.get('configs') or []

        if len(configs) > 0 or len(disks) > 0:
            self.__wait_for_instance_status(
                self._instance,
                {'offline', 'running'},
                self.module.params.get('wait_timeout'))

            self.__update_disks()
            self.__update_configs()

        if self.module.params.get('booted') is not None:
            self.__handle_instance_boot()

        self._instance._api_get()
        inst_result = self._instance._raw_json
        inst_result['root_pass'] = self._root_pass

        self.results['instance'] = inst_result
        self.results['configs'] = paginated_list_to_json(self._instance.configs)
        self.results['disks'] = paginated_list_to_json(self._instance.disks)

    def __handle_absent(self) -> None:
        """Destroys the instance defined in kwargs"""
        label = self.module.params.get('label')

        self._instance = self.__get_instance_by_label(label)

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
            self.__handle_absent()
            return self.results

        self.__handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode instance module"""

    LinodeInstance()


if __name__ == '__main__':
    main()
