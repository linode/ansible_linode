#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Instance info."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    create_filter_and,
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Instance

linode_instance_info_spec = {
    # We need to overwrite attributes to exclude them as requirements
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.integer,
        required=False,
        conflicts_with=["label"],
        description=[
            "The unique ID of the instance.",
            "Optional if `label` is defined.",
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=False,
        conflicts_with=["id"],
        description=[
            "The instance’s label.",
            "Optional if `id` is defined.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode Instance."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_instance_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "instance": SpecReturnValue(
            description="The instance description in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/linode-instances/#linode-view__responses",
            type=FieldType.dict,
            sample=docs_parent.result_instance_samples,
        ),
        "configs": SpecReturnValue(
            description="A list of configs tied to this Linode Instance.",
            docs_url="https://www.linode.com/docs/api/linode-instances/"
            "#configuration-profile-view__responses",
            type=FieldType.list,
            sample=docs_parent.result_configs_samples,
        ),
        "disks": SpecReturnValue(
            description="A list of disks tied to this Linode Instance.",
            docs_url="https://www.linode.com/docs/api/linode-instances/#disk-view__responses",
            type=FieldType.list,
            sample=docs_parent.result_disks_samples,
        ),
        "networking": SpecReturnValue(
            description="Networking information about this Linode Instance.",
            docs_url="https://www.linode.com/docs/api/linode-instances/"
            "#networking-information-list__responses",
            type=FieldType.dict,
            sample=docs_parent.result_networking_samples,
        ),
    },
)

linode_instance_valid_filters = ["id", "label"]


class LinodeInstanceInfo(LinodeModuleBase):
    """Module for getting info about a Linode Instance"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results: Dict[str, Any] = {
            "instance": None,
            "configs": None,
            "disks": None,
            "networking": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_matching_instance(self) -> Optional[Instance]:
        params = self.module.params

        filter_items = {
            k: v
            for k, v in params.items()
            if k in linode_instance_valid_filters and v is not None
        }

        filter_statement = create_filter_and(Instance, filter_items)

        try:
            # Special case because ID is not filterable
            if "id" in filter_items.keys():
                result = Instance(self.client, params.get("id"))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.linode.instances(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg="failed to get instance {0}".format(exception))

    def _get_networking(self, inst: Instance) -> Dict[str, Any]:
        return self.client.get("/linode/instances/{0}/ips".format(inst.id))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for instance info module"""

        instance = self._get_matching_instance()

        if instance is None:
            return self.fail("failed to get instance")

        self.results["instance"] = instance._raw_json
        self.results["configs"] = paginated_list_to_json(instance.configs)
        self.results["disks"] = paginated_list_to_json(instance.disks)
        self.results["networking"] = self._get_networking(instance)

        return self.results


def main() -> None:
    """Constructs and calls the Linode Instance info module"""
    LinodeInstanceInfo()


if __name__ == "__main__":
    main()
