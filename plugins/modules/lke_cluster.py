#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

import copy
from typing import Any, List, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_cluster as docs
import polling
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values_recursive,
    handle_updates,
    jsonify_node_pool,
    poll_condition,
    validate_required,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ApiError, LKECluster

linode_lke_cluster_autoscaler = {
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

linode_lke_cluster_disk = {
    "size": SpecField(
        type=FieldType.integer,
        description=["This Node Pool’s custom disk layout."],
        required=True,
    ),
    "type": SpecField(
        type=FieldType.string,
        description=["This custom disk partition’s filesystem type."],
        choices=["raw", "ext4"],
    ),
}

linode_lke_cluster_node_pool_spec = {
    "count": SpecField(
        type=FieldType.integer,
        editable=True,
        description=["The number of nodes in the Node Pool."],
        required=True,
    ),
    "type": SpecField(
        type=FieldType.string,
        description=["The Linode Type for all of the nodes in the Node Pool."],
        required=True,
    ),
    "autoscaler": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "When enabled, the number of nodes autoscales within the "
            "defined minimum and maximum values."
        ],
        suboptions=linode_lke_cluster_autoscaler,
    ),
}

linode_lke_cluster_spec = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This Kubernetes cluster’s unique label."],
    ),
    "k8s_version": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The desired Kubernetes version for this Kubernetes "
            "cluster in the format of <major>.<minor>, and the "
            "latest supported patch version will be deployed.",
            "A version upgrade requires that you manually recycle the nodes in your cluster.",
        ],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["This Kubernetes cluster’s location."],
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=["An array of tags applied to the Kubernetes cluster."],
    ),
    "high_availability": SpecField(
        type=FieldType.bool,
        editable=True,
        description=[
            "Defines whether High Availability is enabled for the "
            "Control Plane Components of the cluster. "
        ],
        default=False,
    ),
    "node_pools": SpecField(
        editable=True,
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=linode_lke_cluster_node_pool_spec,
        description=["A list of node pools to configure the cluster with"],
    ),
    "skip_polling": SpecField(
        type=FieldType.bool,
        description=[
            "If true, the module will not wait for all nodes in the cluster to be ready."
        ],
        default=False,
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The period to wait for the cluster to be ready in seconds."
        ],
        default=600,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode LKE clusters."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_lke_cluster_spec,
    examples=docs.examples,
    return_values={
        "cluster": SpecReturnValue(
            description="The LKE cluster in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/linode-kubernetes-engine-lke/"
            "#kubernetes-cluster-view__response-samples",
            type=FieldType.dict,
            sample=docs.result_cluster,
        ),
        "node_pools": SpecReturnValue(
            description="A list of node pools in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/linode-kubernetes-engine-lke/"
            "#node-pools-list__response-samples",
            type=FieldType.list,
            sample=docs.result_node_pools,
        ),
        "kubeconfig": SpecReturnValue(
            description="The Base64-encoded kubeconfig used to access this cluster. \n"
            "NOTE: This value may be unavailable if `skip_polling` is true.",
            docs_url="https://www.linode.com/docs/api/linode-kubernetes-engine-lke/"
            "#kubeconfig-view__responses",
            type=FieldType.string,
        ),
        "dashboard_url": SpecReturnValue(
            description="The Cluster Dashboard access URL.",
            docs_url="https://www.linode.com/docs/api/linode-kubernetes-engine-lke/"
            "#kubernetes-cluster-dashboard-url-view__responses",
            type=FieldType.string,
        ),
    },
)

MUTABLE_FIELDS: Set[str] = {"tags"}

REQUIRED_PRESENT: Set[str] = {"k8s_version", "region", "label", "node_pools"}

CREATE_FIELDS: Set[str] = {
    "label",
    "region",
    "tags",
    "k8s_version",
    "node_pools",
    "control_plane",
    "high_availability",
}


class LinodeLKECluster(LinodeModuleBase):
    """Module for creating and destroying Linode LKE clusters"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "cluster": None,
            "node_pools": None,
            "dashboard_url": None,
            "kubeconfig": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_cluster_by_name(self, name: str) -> Optional[LKECluster]:
        try:
            clusters = self.client.lke.clusters()

            for cluster in clusters:
                if cluster.label == name:
                    return cluster

            return None
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get lke cluster {0}: {1}".format(name, exception)
            )

    def _wait_for_all_nodes_ready(
        self, cluster: LKECluster, timeout: int
    ) -> None:
        def _check_cluster_nodes_ready() -> bool:
            for pool in cluster.pools:
                for node in pool.nodes:
                    if node.status != "ready":
                        return False
            return True

        try:
            polling.poll(
                _check_cluster_nodes_ready,
                step=4,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail("failed to wait for lke cluster: timeout period expired")

    def _create_cluster(self) -> Optional[LKECluster]:
        params = filter_null_values_recursive(self.module.params)

        label = params.pop("label")

        # We want HA to be a root-level attribute in ansible
        high_avail = params.pop("high_availability")

        params["control_plane"] = {"high_availability": high_avail}

        # Let's filter down to valid keys
        params = {k: v for k, v in params.items() if k in CREATE_FIELDS}

        try:
            self.register_action("Created LKE cluster {0}".format(label))

            # This is necessary to use fields not yet supported by linode_api4
            result = self.client.lke.cluster_create(
                params.pop("region"),
                label,
                params.pop("node_pools"),
                params.pop("k8s_version"),
                **params,
            )

            return result
        except Exception as exception:
            return self.fail(
                msg="failed to create lke cluster: {0}".format(exception)
            )

    def _cluster_put_updates(self, cluster: LKECluster) -> None:
        """Handles manual field updates for the current LKE cluster"""

        should_update = False

        # version upgrade
        k8s_version = self.module.params.get("k8s_version")

        if cluster.k8s_version.id != k8s_version:
            cluster.k8s_version = k8s_version
            should_update = True

            self.register_action(
                "Upgraded cluster {} -> {}".format(
                    cluster.k8s_version.id, k8s_version
                )
            )

        # HA upgrade
        high_avail = self.module.params.get("high_availability")
        current_ha = cluster.control_plane.high_availability

        if current_ha != high_avail:
            if not high_avail:
                self.fail("Clusters cannot be downgraded from ha")

            cluster.control_plane = {
                "high_availability": high_avail,
            }
            should_update = True

        if should_update:
            cluster.save()

    def _update_cluster(self, cluster: LKECluster) -> None:
        """Handles all update functionality for the current LKE cluster"""

        new_params = filter_null_values_recursive(
            copy.deepcopy(self.module.params)
        )
        new_params = {k: v for k, v in new_params.items() if k in CREATE_FIELDS}

        pools = new_params.pop("node_pools")

        # These are handled separately
        new_params.pop("k8s_version")
        new_params.pop("high_availability")

        handle_updates(
            cluster, new_params, MUTABLE_FIELDS, self.register_action
        )

        self._cluster_put_updates(cluster)

        existing_pools = copy.deepcopy(cluster.pools)
        should_keep = [False for _ in existing_pools]
        pools_handled = [False for _ in pools]

        for k, pool in enumerate(pools):
            for i, current_pool in enumerate(existing_pools):
                if should_keep[i]:
                    continue

                # pool already exists
                if (
                    current_pool.count == pool["count"]
                    and current_pool.type.id == pool["type"]
                ):
                    if (
                        "autoscaler" in pool
                        and current_pool.autoscaler != pool["autoscaler"]
                    ):
                        self.register_action(
                            "Updated autoscaler for Node Pool {}".format(
                                current_pool.id
                            )
                        )

                        current_pool.autoscaler = pool.get("autoscaler")
                        current_pool.save()

                    pools_handled[k] = True
                    should_keep[i] = True
                    break

        for i, pool in enumerate(pools):
            if pools_handled[i]:
                continue

            created = False

            for k, existing_pool in enumerate(existing_pools):
                if should_keep[k]:
                    continue

                if existing_pool.type.id == pool["type"]:
                    # We found a match
                    should_update = False

                    if existing_pool.count != pool["count"]:
                        self.register_action(
                            "Resized pool {} from {} -> {}".format(
                                existing_pool.id,
                                existing_pool.count,
                                pool["count"],
                            )
                        )

                        existing_pool.count = pool["count"]
                        should_update = True

                    if (
                        "autoscaler" in pool
                        and existing_pool.autoscaler != pool["autoscaler"]
                    ):
                        self.register_action(
                            "Updated autoscaler for Node Pool {}".format(
                                existing_pool.id
                            )
                        )
                        existing_pool.autoscaler = pool["autoscaler"]
                        should_update = True

                    if should_update:
                        existing_pool.save()

                    should_keep[k] = True

                    created = True
                    break

            if not created:
                self.register_action(
                    "Created pool with {} nodes and type {}".format(
                        pool["count"], pool["type"]
                    )
                )

                cluster.node_pool_create(
                    pool["type"],
                    pool["count"],
                    autoscaler=pool.get("autoscaler"),
                )

        for i, pool in enumerate(existing_pools):
            if should_keep[i]:
                continue

            self.register_action("Deleted pool {}".format(pool.id))
            pool.delete()

    def _populate_kubeconfig_no_poll(self, cluster: LKECluster) -> None:
        try:
            self.results["kubeconfig"] = cluster.kubeconfig
        except ApiError as error:
            if error.status != 503:
                raise error

            self.results["kubeconfig"] = "Kubeconfig not yet available..."

    def _populate_kubeconfig_poll(self, cluster: LKECluster) -> None:
        def condition() -> bool:
            try:
                self.results["kubeconfig"] = cluster.kubeconfig
            except ApiError as error:
                if error.status != 503:
                    raise error

                return False

            return True

        poll_condition(condition, 4, self._timeout_ctx.seconds_remaining)

    def _populate_dashboard_url_no_poll(self, cluster: LKECluster) -> None:
        try:
            self.results["dashboard_url"] = cluster.cluster_dashboard_url_view()
        except ApiError as error:
            if error.status != 503:
                raise error

            self.results["dashboard_url"] = "Dashboard URL not yet available..."

    def _populate_dashboard_url_poll(self, cluster: LKECluster) -> None:
        def condition() -> bool:
            try:
                self.results[
                    "dashboard_url"
                ] = cluster.cluster_dashboard_url_view()
            except ApiError as error:
                if error.status != 503:
                    raise error

                return False

            return True

        poll_condition(condition, 1, self._timeout_ctx.seconds_remaining)

    def _populate_results(self, cluster: LKECluster) -> None:
        cluster._api_get()

        self.results["cluster"] = cluster._raw_json
        self.results["node_pools"] = [
            jsonify_node_pool(pool) for pool in cluster.pools
        ]

        # We want to skip polling if designated
        if (
            self.module.params.get("skip_polling")
            or self.module.params.get("state") == "absent"
        ):
            self._populate_kubeconfig_no_poll(cluster)
            self._populate_dashboard_url_no_poll(cluster)
            return

        self._populate_kubeconfig_poll(cluster)
        self._populate_dashboard_url_poll(cluster)

    def _handle_present(self) -> None:
        params = self.module.params

        try:
            validate_required(REQUIRED_PRESENT, params)
        except Exception as exception:
            self.fail(exception)

        label: str = params.get("label")

        cluster = self._get_cluster_by_name(label)

        # Create the domain if it does not already exist
        if cluster is None:
            cluster = self._create_cluster()

        self._update_cluster(cluster)

        # Force lazy-loading
        cluster._api_get()

        if not params.get("skip_polling"):
            self._wait_for_all_nodes_ready(
                cluster, self._timeout_ctx.seconds_remaining
            )

        self._populate_results(cluster)

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        cluster = self._get_cluster_by_name(label)

        if cluster is not None:
            self._populate_results(cluster)

            cluster.delete()
            self.register_action("Deleted cluster {0}".format(cluster))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Domain module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeLKECluster()


if __name__ == "__main__":
    main()
