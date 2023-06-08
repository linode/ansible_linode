#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode instances."""

from __future__ import absolute_import, division, print_function

import copy
from typing import Any, Dict, List, Optional, Union, cast

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_event_poller import (
    EventPoller,
    wait_for_resource_free,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    drop_empty_strings,
    filter_null_values,
    filter_null_values_recursive,
    paginated_list_to_json,
    parse_linode_types,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

try:
    from linode_api4 import Config, ConfigInterface, Disk, Instance, Volume
except ImportError:
    # handled in module_utils.linode_common
    pass

linode_instance_disk_spec = {
    "authorized_keys": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of SSH public key parts to deploy for the root user."
        ],
    ),
    "authorized_users": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=["A list of usernames."],
    ),
    "filesystem": SpecField(
        type=FieldType.string,
        description=["The filesystem to create this disk with."],
    ),
    "image": SpecField(
        type=FieldType.string,
        description=["An Image ID to deploy the Disk from."],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["The label to give this Disk."],
    ),
    "root_pass": SpecField(
        type=FieldType.string,
        description=["The root user’s password on the newly-created Linode."],
    ),
    "size": SpecField(
        type=FieldType.integer,
        required=True,
        editable=True,
        description=["The size of the Disk in MB."],
    ),
    "stackscript_id": SpecField(
        type=FieldType.integer,
        description=[
            "The ID of the StackScript to use when creating the instance.",
            "See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).",
        ],
    ),
    "stackscript_data": SpecField(
        type=FieldType.dict,
        description=[
            "An object containing arguments to any User Defined Fields present in "
            "the StackScript used when creating the instance.",
            "Only valid when a stackscript_id is provided.",
            "See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).",
        ],
    ),
}

linode_instance_device_spec = {
    "disk_label": SpecField(
        type=FieldType.string,
        description=["The label of the disk to attach to this Linode."],
    ),
    "disk_id": SpecField(
        type=FieldType.integer,
        description=["The ID of the disk to attach to this Linode."],
    ),
    "volume_id": SpecField(
        type=FieldType.integer,
        description=["The ID of the volume to attach to this Linode."],
    ),
}

linode_instance_devices_spec = {
    f"sd{k}": SpecField(
        type=FieldType.dict,
        description=[f"The device to be mapped to /dev/sd{k}"],
        suboptions=linode_instance_device_spec,
    )
    for k in "abcdefgh"
}

linode_instance_helpers_spec = {
    "devtmpfs_automount": SpecField(
        type=FieldType.bool,
        description=[
            "Populates the /dev directory early during boot without udev."
        ],
    ),
    "distro": SpecField(
        type=FieldType.bool,
        description=["Helps maintain correct inittab/upstart console device."],
    ),
    "modules_dep": SpecField(
        type=FieldType.bool,
        description=[
            "Creates a modules dependency file for the Kernel you run."
        ],
    ),
    "network": SpecField(
        type=FieldType.bool,
        description=["Automatically configures static networking."],
    ),
    "updatedb_disabled": SpecField(
        type=FieldType.bool,
        description=["Disables updatedb cron job to avoid disk thrashing."],
    ),
}

linode_instance_interface_spec = {
    "purpose": SpecField(
        type=FieldType.string,
        required=True,
        description=["The type of interface."],
        choices=["public", "vlan"],
    ),
    "label": SpecField(
        type=FieldType.string,
        description=[
            "The name of this interface.",
            "Required for vlan purpose interfaces.",
            "Must be an empty string or null for public purpose interfaces.",
        ],
    ),
    "ipam_address": SpecField(
        type=FieldType.string,
        description=[
            "This Network Interface’s private IP address in Classless "
            "Inter-Domain Routing (CIDR) notation."
        ],
    ),
}

linode_instance_config_spec = {
    "comments": SpecField(
        type=FieldType.string,
        editable=True,
        description=["Arbitrary User comments on this Config."],
    ),
    "devices": SpecField(
        type=FieldType.dict,
        required=True,
        suboptions=linode_instance_devices_spec,
        description=["The devices to map to this configuration."],
    ),
    "helpers": SpecField(
        type=FieldType.dict,
        suboptions=linode_instance_helpers_spec,
        description=["Helpers enabled when booting to this Linode Config."],
    ),
    "kernel": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            'A Kernel ID to boot a Linode with. Defaults to "linode/latest-64bit".'
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["The label to assign to this config."],
    ),
    "memory_limit": SpecField(
        type=FieldType.integer,
        editable=True,
        description=["Defaults to the total RAM of the Linode."],
    ),
    "root_device": SpecField(
        type=FieldType.string,
        editable=True,
        description=["The root device to boot."],
    ),
    "run_level": SpecField(
        type=FieldType.string,
        editable=True,
        description=["Defines the state of your Linode after booting."],
    ),
    "virt_mode": SpecField(
        type=FieldType.string,
        editable=True,
        description=["Controls the virtualization mode."],
        choices=["paravirt", "fullvirt"],
    ),
    "interfaces": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_instance_interface_spec,
        editable=True,
        description=[
            "A list of network interfaces to apply to the Linode.",
            "See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances"
            "/#configuration-profile-create__request-body-schema).",
        ],
    ),
}

spec_additional_ipv4 = {
    "public": SpecField(
        type=FieldType.bool,
        description="Whether the allocated IPv4 address should be public or private.",
        required=True,
    )
}

linode_instance_spec = {
    "label": SpecField(
        type=FieldType.string,
        description=["The unique label to give this instance."],
    ),
    "type": SpecField(
        type=FieldType.string,
        description=["The Linode Type of the Linode you are creating."],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=[
            "The location to deploy the instance in.",
            "See the [Linode API documentation](https://api.linode.com/v4/regions).",
        ],
    ),
    "image": SpecField(
        type=FieldType.string,
        conflicts_with=["disks", "configs"],
        description=["The image ID to deploy the instance disk from."],
    ),
    "authorized_keys": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of SSH public key parts to deploy for the root user."
        ],
    ),
    "root_pass": SpecField(
        type=FieldType.string,
        no_log=True,
        description=[
            "The password for the root user.",
            "If not specified, one will be generated.",
            "This generated password will be available in the task success JSON.",
        ],
    ),
    "stackscript_id": SpecField(
        type=FieldType.integer,
        description=[
            "The ID of the StackScript to use when creating the instance.",
            "See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).",
        ],
    ),
    "stackscript_data": SpecField(
        type=FieldType.dict,
        description=[
            "An object containing arguments to any User Defined Fields present in "
            "the StackScript used when creating the instance.",
            "Only valid when a stackscript_id is provided.",
            "See the [Linode API documentation](https://www.linode.com/docs/api/stackscripts/).",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "private_ip": SpecField(
        type=FieldType.bool,
        description=[
            "If true, the created Linode will have private networking enabled."
        ],
    ),
    "group": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The group that the instance should be marked under.",
            "Please note, that group labelling is deprecated but still supported.",
            "The encouraged method for marking instances is to use tags.",
        ],
    ),
    "boot_config_label": SpecField(
        type=FieldType.string,
        description=["The label of the config to boot from."],
    ),
    "configs": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_instance_config_spec,
        editable=True,
        conflicts_with=["image", "interfaces"],
        description=[
            "A list of Instance configs to apply to the Linode.",
            "See the [Linode API documentation](https://www.linode.com/docs"
            "/api/linode-instances/#configuration-profile-create).",
        ],
    ),
    "disks": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_instance_disk_spec,
        editable=True,
        conflicts_with=["image", "interfaces"],
        description=[
            "A list of Disks to create on the Linode.",
            "See the [Linode API documentation](https://www.linode.com/"
            "docs/api/linode-instances/#disk-create).",
        ],
    ),
    "interfaces": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_instance_interface_spec,
        conflicts_with=["disks", "configs"],
        description=[
            "A list of network interfaces to apply to the Linode.",
            "See the [Linode API documentation](https://www.linode.com/docs/api/linode-instances/"
            "#linode-create__request-body-schema).",
        ],
    ),
    "booted": SpecField(
        type=FieldType.bool,
        description=[
            "Whether the new Instance should be booted.",
            "This will default to True if the Instance is deployed from an Image or Backup.",
        ],
    ),
    "backup_id": SpecField(
        type=FieldType.integer,
        description=[
            "The id of the Backup to restore to the new Instance.",
            'May not be provided if "image" is given.',
        ],
    ),
    "wait": SpecField(
        type=FieldType.bool,
        default=True,
        description=[
            'Wait for the instance to have status "running" before returning.'
        ],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        default=240,
        description=[
            "The amount of time, in seconds, to wait for an instance to "
            'have status "running".'
        ],
    ),
    "additional_ipv4": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=spec_additional_ipv4,
        description=["Additional ipv4 addresses to allocate."],
        editable=False,
    ),
    "rebooted": SpecField(
        type=FieldType.bool,
        description=[
            "If true, the Linode Instance will be rebooted.",
            "NOTE: The instance will only be rebooted if it was "
            "previously in a running state.",
            "To ensure your Linode will always be rebooted, consider "
            "also setting the `booted` field.",
        ],
        default=False,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode Instances, Configs, and Disks."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_instance_spec,
    examples=docs.specdoc_examples,
    return_values={
        "instance": SpecReturnValue(
            description="The instance description in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/linode-instances/#linode-view__responses",
            type=FieldType.dict,
            sample=docs.result_instance_samples,
        ),
        "configs": SpecReturnValue(
            description="A list of configs tied to this Linode Instance.",
            docs_url="https://www.linode.com/docs/api/linode-instances/"
            "#configuration-profile-view__responses",
            type=FieldType.list,
            sample=docs.result_configs_samples,
        ),
        "disks": SpecReturnValue(
            description="A list of disks tied to this Linode Instance.",
            docs_url="https://www.linode.com/docs/api/linode-instances/#disk-view__responses",
            type=FieldType.list,
            sample=docs.result_disks_samples,
        ),
        "networking": SpecReturnValue(
            description="Networking information about this Linode Instance.",
            docs_url="https://www.linode.com/docs/api/linode-instances/"
            "#networking-information-list__responses",
            type=FieldType.dict,
            sample=docs.result_networking_samples,
        ),
    },
)

# Fields that can be updated on an existing instance
linode_instance_mutable = {"group", "tags"}

linode_instance_config_mutable = {
    "comments",
    "kernel",
    "memory_limit",
    "root_device",
    "run_level",
    "virt_mode",
    "interfaces",
}


class LinodeInstance(LinodeModuleBase):
    """Module for creating and destroying Linode Instances"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec

        self.mutually_exclusive = [
            ("image", "disks"),
            ("image", "configs"),
            ("interfaces", "configs"),
            ("interfaces", "disks"),
        ]

        self.results = {
            "changed": False,
            "actions": [],
            "instance": None,
            "configs": None,
            "networking": None,
        }

        self._instance: Optional[Instance] = None
        self._root_pass: str = ""

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            mutually_exclusive=self.mutually_exclusive,
        )

    def _get_instance_by_label(self, label: str) -> Optional[Instance]:
        """Gets a Linode instance by label"""

        try:
            return self.client.linode.instances(Instance.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get instance {0}: {1}".format(label, exception)
            )

    def _get_desired_instance_status(self) -> str:
        booted = self.module.params.get("booted")
        disks = self.module.params.get("disks")
        configs = self.module.params.get("configs")

        if (
            not booted
            or (disks is not None and len(disks) > 0)
            or (configs is not None and len(configs) > 0)
        ):
            return "offline"

        return "running"

    def _get_boot_config(self) -> Optional[Config]:
        config_label = self.module.params.get("boot_config_label")

        if config_label is not None:
            # Find the config with the matching label
            return next(
                (
                    config
                    for config in self._instance.configs
                    if config.label == config_label
                ),
                None,
            )

        if len(self._instance.configs) > 0:
            return self._instance.configs[0]

        return None

    def _get_disk_by_label(self, label: str) -> Optional[Disk]:
        # Find the disk with the matching label
        return next(
            (disk for disk in self._instance.disks if disk.label == label), None
        )

    def _get_networking(self) -> Dict[str, Any]:
        return self.client.get(
            "/linode/instances/{0}/ips".format(self._instance.id)
        )

    @staticmethod
    def _device_to_param_mapping(device: Union[Disk, Volume]) -> Dict[str, int]:
        id_key = ""

        if isinstance(device, Volume):
            id_key = "volume_id"

        if isinstance(device, Disk):
            id_key = "disk_id"

        return {id_key: device.id}

    def _compare_param_to_device(
        self, device_param: Dict[str, Any], device: Union[Disk, Volume]
    ) -> bool:
        if device is None or device_param is None:
            return device == device_param

        device_mapping = self._device_to_param_mapping(device)

        disk_label = device_param.get("disk_label")
        if disk_label is not None:
            disk = self._get_disk_by_label(disk_label)
            if disk is None:
                self.fail(msg="invalid disk specified")

            device_param = {"disk_id": disk.id}

        return filter_null_values(device_mapping) == filter_null_values(
            device_param
        )

    def _create_instance(self) -> dict:
        """Creates a Linode instance"""
        params = copy.deepcopy(self.module.params)

        if "root_pass" in params.keys() and params.get("root_pass") is None:
            params.pop("root_pass")

        ltype = params.pop("type")
        region = params.pop("region")

        result = {"instance": None, "root_pass": ""}

        # We want to retry on 408s
        response = self.client.linode.instance_create(ltype, region, **params)

        # Weird variable return type
        if isinstance(response, tuple):
            result["instance"] = response[0]
            result["root_pass"] = response[1]
        else:
            result["instance"] = response

        return result

    def _param_device_to_device(
        self, device: Dict[str, Any]
    ) -> Union[Disk, Volume, None]:
        if device is None:
            return None

        disk_label = device.get("disk_label")
        disk_id = device.get("disk_id")
        volume_id = device.get("volume_id")

        if disk_label is not None:
            disk = self._get_disk_by_label(disk_label)
            if disk is None:
                self.fail(msg="invalid disk label: {0}".format(disk_label))

            return disk

        if disk_id is not None:
            return Disk(self.client, device.get("disk_id"), self._instance.id)

        if volume_id is not None:
            return Volume(self.client, device.get("volume_id"))

        return None

    def _create_config_register(self, config_params: Dict[str, Any]) -> None:
        device_params = config_params.pop("devices")
        devices = []

        if device_params is not None:
            for device_suffix in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                device_name = "sd{0}".format(device_suffix)
                if device_name not in device_params:
                    continue

                device_dict = device_params.get(device_name)
                devices.append(self._param_device_to_device(device_dict))

        try:
            self._instance.config_create(
                devices=devices, **filter_null_values(config_params)
            )
        except ValueError as err:
            self.fail(msg=";".join(err.args))

        self.register_action(
            "Created config {0}".format(config_params.get("label"))
        )

    def _delete_config_register(self, config: Config) -> None:
        self.register_action("Deleted config {0}".format(config.label))
        config.delete()

    def _create_disk_register(self, **kwargs: Any) -> None:
        size = kwargs.pop("size")

        create_poller = EventPoller(
            self.client, "disks", "disk_create", entity_id=self._instance.id
        )
        self._instance.disk_create(size, **kwargs)

        # The disk must be ready before the next disk is created
        create_poller.wait_for_next_event_finished(
            self._timeout_ctx.seconds_remaining
        )

        self.register_action("Created disk {0}".format(kwargs.get("label")))

    def _delete_disk_register(self, disk: Disk) -> None:
        self.register_action("Deleted disk {0}".format(disk.label))
        disk.delete()

    def _update_interfaces(self) -> None:
        config = self._get_boot_config()
        param_interfaces: List[Any] = self.module.params.get("interfaces")

        if config is None or param_interfaces is None:
            return

        param_interfaces = [drop_empty_strings(v) for v in param_interfaces]
        remote_interfaces = [
            drop_empty_strings(v._serialize()) for v in config.interfaces
        ]

        if remote_interfaces == param_interfaces:
            return

        config.interfaces = [ConfigInterface(**v) for v in param_interfaces]
        config.save()

        self.register_action(
            "Updated interfaces for instance {0} config {1}".format(
                self._instance.label, config.id
            )
        )

    def _update_config(
        self, config: Config, config_params: Dict[str, Any]
    ) -> None:
        should_update = False
        params = filter_null_values(config_params)

        for key, new_value in params.items():
            if not hasattr(config, key):
                continue

            old_value = parse_linode_types(getattr(config, key))

            # Special handling for the ConfigInterface type
            if key == "interfaces":
                old_value = filter_null_values_recursive(
                    [drop_empty_strings(v._serialize()) for v in old_value]
                )
                new_value = filter_null_values_recursive(
                    [drop_empty_strings(v) for v in new_value]
                )

            # Special diffing due to handling in linode_api4-python
            if key == "devices":
                for device_key, device in old_value.items():
                    if not self._compare_param_to_device(
                        new_value[device_key], device
                    ):
                        self.fail(
                            msg="failed to update config: {0} is a non-mutable field".format(
                                "devices"
                            )
                        )

                continue

            if new_value != old_value:
                if key in linode_instance_config_mutable:
                    setattr(config, key, new_value)
                    self.register_action(
                        'Updated Config {0}: "{1}" -> "{2}"'.format(
                            key, old_value, new_value
                        )
                    )
                    should_update = True
                    continue

                self.fail(
                    msg="failed to update config: {0} is a non-mutable field".format(
                        key
                    )
                )

        if should_update:
            config.save()

    def _update_configs(self) -> None:
        current_configs = self._instance.configs

        if self.module.params.get("image") is not None:
            return

        config_params = self.module.params["configs"] or []
        config_map: Dict[str, Config] = {}

        for config in current_configs:
            config_map[config.label] = config

        for config in config_params:
            config_label = config["label"]

            if config_label in config_map:
                self._update_config(config_map[config_label], config)

                del config_map[config_label]
                continue

            self._create_config_register(config)

        for config in config_map.values():
            self._delete_config_register(config)

    def _update_disk(self, disk: Disk, disk_params: Dict[str, Any]) -> None:
        new_size = disk_params.pop("size")

        if disk.size != new_size:
            resize_poller = EventPoller(
                self.client, "disks", "disk_resize", entity_id=self._instance.id
            )

            disk.resize(new_size)

            resize_poller.wait_for_next_event_finished(
                self._timeout_ctx.seconds_remaining
            )

            self.register_action(
                "Resized disk {0}: {1} -> {2}".format(
                    disk.label, disk.size, new_size
                )
            )
            disk._api_get()

        for key, new_value in filter_null_values(disk_params).items():
            if not hasattr(disk, key):
                continue

            old_value = getattr(disk, key)
            if new_value != old_value:
                self.fail(
                    msg="failed to update disk: {0} is a non-mutable field".format(
                        key
                    )
                )

    def _update_disks(self) -> None:
        current_disks = self._instance.disks

        # Instances with implicit disks should be ignored
        if self.module.params.get("image") is not None:
            return

        disk_params = self.module.params["disks"] or []

        disk_map: Dict[str, Disk] = {}

        for disk in current_disks:
            disk_map[disk.label] = disk

        for disk in disk_params:
            disk_label = disk["label"]

            if disk_label in disk_map:
                self._update_disk(disk_map[disk_label], disk)

                del disk_map[disk_label]
                continue

            self._create_disk_register(**disk)

        if len(disk_map.values()) > 0:
            self.fail(
                msg="unable to update disks: disks must be removed manually"
            )

    def _update_instance(self) -> None:
        """Update instance handles all update functionality for the current instance"""
        should_update = False

        params = filter_null_values(self.module.params)

        for key, new_value in params.items():
            if not hasattr(self._instance, key):
                continue

            if key in {"configs", "disks", "boot_config_label", "reboot"}:
                continue

            old_value = parse_linode_types(getattr(self._instance, key))

            if new_value != old_value:
                if key in linode_instance_mutable:
                    setattr(self._instance, key, new_value)
                    self.register_action(
                        'Updated instance {0}: "{1}" -> "{2}"'.format(
                            key, old_value, new_value
                        )
                    )

                    should_update = True
                    continue

                self.fail(
                    "failed to update instance {0}: {1} is a non-updatable field".format(
                        self._instance.label, key
                    )
                )

        if should_update:
            self._instance.save()

        needs_private_ip = self.module.params.get("private_ip")
        additional_ipv4 = self.module.params.get("additional_ipv4")

        if needs_private_ip or additional_ipv4:
            ipv4_length = len(additional_ipv4 or [])

            min_ips = 2 if needs_private_ip else 1
            if ipv4_length != len(getattr(self._instance, "ipv4")) - min_ips:
                self.fail(
                    "failed to update instance {0}: additional_ipv4 is a "
                    "non-updatable field".format(self._instance.label)
                )

        # Update interfaces
        self._update_interfaces()

    def _handle_instance_boot(self) -> None:
        boot_status = self.module.params.get("booted")
        should_poll = self.module.params.get("wait")

        # Wait for instance to not be busy
        wait_for_resource_free(
            self.client,
            "linode",
            self._instance.id,
            self._timeout_ctx.seconds_remaining,
        )

        self._instance._api_get()

        event_poller = None

        if boot_status and self._instance.status != "running":
            event_poller = EventPoller(
                self.client,
                "linode",
                "linode_boot",
                entity_id=self._instance.id,
            )

            self._instance.boot(self._get_boot_config())
            self.register_action(
                "Booted instance {0}".format(self.module.params.get("label"))
            )

        if not boot_status and self._instance.status != "offline":
            event_poller = EventPoller(
                self.client,
                "linode",
                "linode_shutdown",
                entity_id=self._instance.id,
            )

            self._instance.shutdown()
            self.register_action(
                "Shutdown instance {0}".format(self.module.params.get("label"))
            )

        if should_poll and event_poller is not None:
            # Poll for the instance to be booted if necessary
            event_poller.wait_for_next_event_finished(
                self._timeout_ctx.seconds_remaining
            )

    def _handle_instance_reboot(self) -> None:
        if not self.module.params.get("rebooted"):
            return

        should_poll = self.module.params.get("wait")

        # Wait for instance to not be busy
        wait_for_resource_free(
            self.client,
            "linode",
            self._instance.id,
            self._timeout_ctx.seconds_remaining,
        )

        self._instance._api_get()

        # We don't want to reboot if the Linode is already offline
        if self._instance.status != "running":
            return

        reboot_poller = EventPoller(
            self.client, "linode", "linode_reboot", entity_id=self._instance.id
        )

        self._instance.reboot()
        self.register_action(
            "Rebooted instance {}".format(self._instance.label)
        )

        if should_poll:
            reboot_poller.wait_for_next_event_finished(
                self._timeout_ctx.seconds_remaining
            )

    def _handle_present(self) -> None:
        """Updates the instance defined in kwargs"""

        label = self.module.params.get("label")
        should_wait = self.module.params.get("wait")

        self._instance = self._get_instance_by_label(label)
        already_exists = self._instance is not None

        if not already_exists:
            create_poller = EventPoller(self.client, "linode", "linode_create")

            result = self._create_instance()

            self._instance = cast(Instance, result.get("instance"))
            self._root_pass = str(result.get("root_pass"))

            self.register_action("Created instance {0}".format(label))

            create_poller.set_entity_id(self._instance.id)

            if should_wait:
                create_poller.wait_for_next_event_finished(
                    self._timeout_ctx.seconds_remaining
                )

            if self.module.params.get("additional_ipv4") is not None:
                additional_ip_types = self.module.params.get("additional_ipv4")

                for ip_type in additional_ip_types:
                    self._instance.ip_allocate(public=ip_type["public"])
        else:
            self._update_instance()

        # Wait for Linode to not be busy if configs or disks need to be created
        # This eliminates the need for unnecessary polling
        disks = self.module.params.get("disks") or []
        configs = self.module.params.get("configs") or []

        if len(configs) > 0 or len(disks) > 0:
            wait_for_resource_free(
                self.client,
                "linode",
                self._instance.id,
                self._timeout_ctx.seconds_remaining,
            )

            self._update_disks()
            self._update_configs()

        # Don't reboot on instance creation
        if self.module.params.get("rebooted") is not None and already_exists:
            self._handle_instance_reboot()

        if self.module.params.get("booted") is not None:
            self._handle_instance_boot()

        self._instance._api_get()
        inst_result = self._instance._raw_json
        inst_result["root_pass"] = self._root_pass

        self.results["instance"] = inst_result
        self.results["configs"] = paginated_list_to_json(self._instance.configs)
        self.results["disks"] = paginated_list_to_json(self._instance.disks)
        self.results["networking"] = self._get_networking()

    def _handle_absent(self) -> None:
        """Destroys the instance defined in kwargs"""
        label = self.module.params.get("label")

        self._instance = self._get_instance_by_label(label)

        if self._instance is not None:
            self.results["instance"] = self._instance._raw_json
            self.results["configs"] = paginated_list_to_json(
                self._instance.configs
            )
            self.results["disks"] = paginated_list_to_json(self._instance.disks)
            self.results["networking"] = self._get_networking()
            self.register_action("Deleted instance {0}".format(label))
            self._instance.delete()

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Instance module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode instance module"""

    LinodeInstance()


if __name__ == "__main__":
    main()
