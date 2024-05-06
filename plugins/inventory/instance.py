#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the logic for the Linode instance inventory module."""

from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type

import os
from typing import Any, Dict, List, Optional, Set, Tuple

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils.six import string_types
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    COLLECTION_USER_AGENT,
)
from linode_api4.objects import Instance

DOCUMENTATION = """
    name: instance
    author:
      - Luke Murphy (@decentral1se)
      - Lena Garber (@LBGarber)
    requirements:
        - python >= 3
        - linode_api4 >= 2.0.0
    description:
        - Reads instance inventories from Linode.
        - Uses a YAML configuration file that ends with linode.(yml|yaml).
        - Linode labels are used by default as the hostnames.
        - The default inventory groups are built from groups (deprecated by
          Linode) and not tags.
    extends_documentation_fragment:
        - constructed
    options:
        plugin:
            description: Marks this as an instance of the 'linode' plugin
            required: true
            choices: ['linode', 'linode.cloud.instance']
        api_token:
            description: The Linode account personal access token.
            required: true
            env:
                - name: LINODE_API_TOKEN
        regions:
          description: Populate inventory with instances in this region.
          default: []
          type: list
        tags:
          description: Populate inventory only with instances which have at least one of the tags listed here.
          default: []
          type: list
        types:
          description: Populate inventory with instances with this type.
          default: []
          type: list
"""

EXAMPLES = """
# Minimal example. `LINODE_API_TOKEN` is exposed in environment.
plugin: linode.cloud.instance

# Example with regions, types, groups and access token
plugin: linode.cloud.instance
api_token: foobar
regions:
  - eu-west
types:
  - g5-standard-2

# Example with keyed_groups, groups, and compose
plugin: linode.cloud.instance
api_token: foobar
keyed_groups:
  - key: tags
    separator: ''
  - key: region
    prefix: region
groups:
  webservers: "'web' in (tags|list)"
  mailservers: "'mail' in (tags|list)"
compose:
  ansible_port: 2222
"""


try:
    from linode_api4 import LinodeClient
    from linode_api4.errors import ApiError as LinodeApiError
    from linode_api4.objects.filtering import Filter

    HAS_LINODE = True
except ImportError:
    HAS_LINODE = False


class InventoryModule(BaseInventoryPlugin, Constructable):
    """Linode instance inventory plugin"""

    NAME = "linode.cloud.instance"

    def __init__(self) -> None:
        super().__init__()
        self.client: Optional[LinodeClient] = None
        self.instances: List[Instance] = []
        self.linode_groups: Set[str] = set()

    def _build_client(self) -> None:
        """Build the Linode client."""

        api_token = self.get_option("api_token")

        if api_token is None:
            try:
                api_token = os.environ["LINODE_API_TOKEN"]
            except KeyError:
                pass

        if self.templar.is_template(api_token):
            api_token = self.templar.template(
                variable=api_token, disable_lookups=False
            )

        if api_token is None:
            raise AnsibleError(
                (
                    "Could not retrieve Linode API Token "
                    "from plugin configuration or environment"
                )
            )

        self.client = LinodeClient(api_token, user_agent=COLLECTION_USER_AGENT)

    def _get_instances_inventory(
        self, regions: List[str], types: List[str], tags: List[str]
    ) -> None:
        """Retrieve Linode instance information from cloud inventory."""
        filters = self._construct_config_filter(regions)

        try:
            if filters:
                self.instances = self.client.linode.instances(filters)
            else:
                self.instances = self.client.linode.instances()
        except LinodeApiError as exception:
            raise AnsibleError(
                "Linode client raised: %s" % exception
            ) from exception

        if types:
            self._filter_instance_types(types)

        if tags:
            self._filter_instance_tags(tags)

    def _add_groups(self) -> None:
        """Add Linode instance groups to the dynamic inventory."""
        self.linode_groups = set(
            filter(None, [instance.group for instance in self.instances])
        )

        for linode_group in self.linode_groups:
            self.inventory.add_group(linode_group)

    @staticmethod
    def _construct_list_filter(attr: str, values: List[str]) -> Dict[str, Any]:
        return {"+or": [{attr: value} for value in values]}

    def _construct_config_filter(self, regions: List[str]) -> Optional[Filter]:
        filters = []

        if regions:
            filters.append(self._construct_list_filter("region", regions))

        if len(filters) < 1:
            return None

        return Filter(
            {
                "+and": filters,
            }
        )

    def _filter_instance_tags(self, valid_tags: List[str]) -> None:
        self.instances = [
            instance
            for instance in self.instances
            if any(tag in instance.tags for tag in valid_tags)
        ]

    def _filter_instance_types(self, valid_types: List[str]) -> None:
        self.instances = [
            instance
            for instance in self.instances
            if instance.type.id in valid_types
        ]

    def _add_instances_to_groups(self) -> None:
        """Add instance names to their dynamic inventory groups."""
        for instance in self.instances:
            self.inventory.add_host(instance.label, group=instance.group)
            self.inventory.set_variable(
                instance.label, "ansible_host", instance.ipv4[0]
            )

    def _add_hostvars_for_instances(self) -> None:
        """Add hostvars for instances in the dynamic inventory."""
        for instance in self.instances:
            hostvars = {}
            hostvars.update(instance._raw_json)
            hostvars["networking_info"] = instance.ips.dict

            for hostvar_key in hostvars:
                self.inventory.set_variable(
                    instance.label, hostvar_key, hostvars[hostvar_key]
                )

    @staticmethod
    def _validate_option(
        name: str, desired_type: Any, option_value: Any
    ) -> Any:
        """Validate user specified configuration data against types."""
        if isinstance(option_value, string_types) and desired_type == list:
            option_value = [option_value]

        if option_value is None:
            option_value = desired_type()

        if not isinstance(option_value, desired_type):
            raise AnsibleParserError(
                "The option %s (%s) must be a %s"
                % (name, option_value, desired_type)
            )

        return option_value

    def _get_query_options(
        self, config_data: Dict[str, Any]
    ) -> Tuple[Any, Any, Any]:
        """Get user specified query options from the configuration."""
        options = {
            "regions": {
                "type_to_be": list,
                "value": config_data.get("regions", []),
            },
            "types": {
                "type_to_be": list,
                "value": config_data.get("types", []),
            },
            "tags": {"type_to_be": list, "value": config_data.get("tags", [])},
        }

        for name in options:
            options[name]["value"] = self._validate_option(
                name, options[name]["type_to_be"], options[name]["value"]
            )

        regions = options["regions"]["value"]
        types = options["types"]["value"]
        tags = options["tags"]["value"]

        return regions, types, tags

    def verify_file(self, path: str) -> bool:
        """Verify the Linode configuration file."""
        if not super().verify_file(path):
            return False

        endings = ("linode.yaml", "linode.yml", "instance.yaml", "instance.yml")
        return any((path.endswith(ending) for ending in endings))

    def parse(
        self, inventory: Any, loader: Any, path: str, cache: bool = True
    ) -> None:
        """Dynamically parse Linode the cloud inventory."""
        super().parse(inventory, loader, path)

        if not HAS_LINODE:
            raise AnsibleError(
                "the Linode dynamic inventory plugin requires linode_api4."
            )

        config_data = self._read_config_data(path)
        self._build_client()

        strict = self.get_option("strict")

        regions, types, tags = self._get_query_options(config_data)
        self._get_instances_inventory(regions, types, tags)

        self._add_groups()
        self._add_instances_to_groups()
        self._add_hostvars_for_instances()

        for instance in self.instances:
            variables = self.inventory.get_host(instance.label).get_vars()
            self._add_host_to_composed_groups(
                self.get_option("groups"),
                variables,
                instance.label,
                strict=strict,
            )
            self._add_host_to_keyed_groups(
                self.get_option("keyed_groups"),
                variables,
                instance.label,
                strict=strict,
            )
            self._set_composite_vars(
                self.get_option("compose"),
                variables,
                instance.label,
                strict=strict,
            )
