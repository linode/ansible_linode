#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode LKE node pools."""

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_node_pool as docs
import linode_api4
import polling
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
    jsonify_node_pool,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import LKENodePool

linode_lke_pool_autoscaler = {
    "enabled": SpecField(
        type=FieldType.bool,
        editable=True,
        description=[
            "Whether autoscaling is enabled for this Node Pool.",
            "NOTE: Subsequent playbook runs will override nodes created by the cluster autoscaler.",
        ],
    ),
    "max": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The maximum number of nodes to autoscale to. "
            "Defaults to the value provided by the count field."
        ],
    ),
    "min": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The minimum number of nodes to autoscale to. "
            "Defaults to the Node Pool’s count."
        ],
    ),
}

linode_lke_pool_disks = {
    "type": SpecField(
        type=FieldType.string,
        required=True,
        description=["This custom disk partition’s filesystem type."],
        choices=["raw", "ext4"],
    ),
    "size": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The size of this custom disk partition in MB."],
    ),
}

MODULE_SPEC = {
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "cluster_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The ID of the LKE cluster that contains this node pool."],
    ),
    "autoscaler": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "When enabled, the number of nodes autoscales within the "
            "defined minimum and maximum values."
        ],
        suboptions=linode_lke_pool_autoscaler,
    ),
    "count": SpecField(
        type=FieldType.integer,
        editable=True,
        description=["The number of nodes in the Node Pool."],
    ),
    "disks": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        description=[
            "This Node Pool’s custom disk layout. "
            "Each item in this array will create a "
            "new disk partition for each node in this "
            "Node Pool."
        ],
        suboptions=linode_lke_pool_disks,
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        required=True,
        description=[
            "An array of tags applied to this object.",
            "Tags must be unique as they are used by the "
            "`lke_node_pool` module to uniquely identify node pools.",
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        description=[
            "The Linode Type for all of the nodes in the Node Pool.",
            "Required if `state` == `present`.",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "skip_polling": SpecField(
        type=FieldType.bool,
        description=[
            "If true, the module will not wait for all "
            "nodes in the node pool to be ready."
        ],
        default=False,
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The period to wait for the node pool to be ready in seconds."
        ],
        default=600,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode LKE cluster node pools."],
    requirements=global_requirements,
    author=global_authors,
    options=MODULE_SPEC,
    examples=docs.examples,
    return_values={
        "node_pool": SpecReturnValue(
            description="The Node Pool in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/linode-kubernetes-engine-lke/"
            "#node-pool-view__response-samples",
            type=FieldType.dict,
            sample=docs.result_node_pool,
        )
    },
)


class LinodeLKENodePool(LinodeModuleBase):
    """Module for managing Linode Firewall devices"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "node_pool": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_node_pool(self) -> Optional[linode_api4.LKENodePool]:
        try:
            params = self.module.params
            cluster_id = params["cluster_id"]
            tags = params["tags"]

            cluster = linode_api4.LKECluster(self.client, cluster_id)
            for pool in cluster.pools:
                if set(pool._raw_json["tags"]) == set(tags):
                    return pool

            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get node pool for cluster {0}: {1}".format(
                    cluster_id, exception
                )
            )

    def _wait_for_all_nodes_ready(
        self, pool: LKENodePool, timeout: int
    ) -> None:
        def _check_pool_nodes_ready() -> bool:
            for node in pool.nodes:
                if node.status != "ready":
                    return False
            return True

        try:
            polling.poll(
                _check_pool_nodes_ready,
                step=4,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail(
                "failed to wait for lke node pool nodes: timeout period expired"
            )

    def _create_pool(self) -> LKENodePool:
        try:
            params = filter_null_values(self.module.params)

            cluster_id = params.pop("cluster_id")
            for key in ["api_token", "api_version"]:
                params.pop(key)

            pool = self.client.post(
                "/lke/clusters/{0}/pools".format(cluster_id), data=params
            )

            pool_obj = LKENodePool(
                self.client, pool["id"], cluster_id, json=pool
            )

            pool_obj._api_get()

            self.register_action("Created node pool {}".format(pool_obj.id))

            return pool_obj
        except Exception as exception:
            return self.fail(
                msg="failed to create lke cluster node pool for cluster {0}: {1}".format(
                    self.module.params.get("cluster_id"), exception
                )
            )

    def _update_pool(self, pool: LKENodePool) -> LKENodePool:
        params = filter_null_values(self.module.params)
        put_data = {}

        cluster_id = params.pop("cluster_id")
        new_autoscaler = (
            params.pop("autoscaler") if "autoscaler" in params else None
        )
        new_count = params.pop("count")

        try:
            handle_updates(pool, params, {}, self.register_action)
        except Exception as exception:
            return self.fail(
                msg="failed to update lke cluster node pool for cluster {0}: {1}".format(
                    cluster_id, exception
                )
            )

        if pool.count != new_count:
            self.register_action(
                "Resized pool from {} -> {}".format(pool.count, new_count)
            )

            put_data["count"] = new_count

        if (
            new_autoscaler is not None
            and pool._raw_json["autoscaler"] != new_autoscaler
        ):
            self.register_action("Updated autoscaler for Node Pool")
            put_data["autoscaler"] = new_autoscaler

        if len(put_data) > 0:
            try:
                self.client.put(
                    "/lke/clusters/{0}/pools/{1}".format(cluster_id, pool.id),
                    data=put_data,
                )
            except Exception as exception:
                return self.fail(
                    msg="failed to update node pool for cluster {0}: {1}".format(
                        cluster_id, exception
                    )
                )

        pool._api_get()

        return pool

    def _handle_present(self) -> None:
        pool = self._get_node_pool()

        # Create the device if it does not already exist
        if pool is None:
            pool = self._create_pool()

        pool = self._update_pool(pool)

        if not self.module.params.get("skip_polling"):
            self._wait_for_all_nodes_ready(
                pool, self._timeout_ctx.seconds_remaining
            )

        self.results["node_pool"] = jsonify_node_pool(pool)

    def _handle_absent(self) -> None:
        pool = self._get_node_pool()

        if pool is not None:
            self.results["node_pool"] = jsonify_node_pool(pool)

            self.register_action(
                "Deleted pool {0} from cluster {1}".format(
                    pool.id, self.module.params["cluster_id"]
                )
            )
            pool.delete()

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for lke_node_pool module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode LKE Node Pool module"""
    LinodeLKENodePool()


if __name__ == "__main__":
    main()
