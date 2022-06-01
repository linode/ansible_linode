#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
from typing import Optional, cast, Any, Set, List, Dict

from linode_api4 import LKECluster, LKENodePool, ApiError

import polling

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    filter_null_values, paginated_list_to_json, jsonify_node_pool, validate_required
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_cluster as docs

from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import handle_updates

linode_lke_cluster_disk = dict(
    size=dict(
        type='int',
        description='This Node Pool’s custom disk layout.',
        required=True
    ),
    type=dict(
        type='str',
        description='This custom disk partition’s filesystem type.',
        choices=['raw', 'ext4']
    )
)

linode_lke_cluster_node_pool_spec = dict(
    count=dict(
        type='int',
        description='The number of nodes in the Node Pool.',
        required=True,
    ),
    type=dict(
        type='str',
        description='The Linode Type for all of the nodes in the Node Pool.',
        required=True,
    )
)

linode_lke_cluster_spec = dict(
    label=dict(
        type='str',
        required=True,
        description='This Kubernetes cluster’s unique label.'
    ),
    k8s_version=dict(
        type='str',
        description='The desired Kubernetes version for this Kubernetes '
                    'cluster in the format of <major>.<minor>, and the '
                    'latest supported patch version will be deployed.'
    ),

    region=dict(
        type='str',
        description='This Kubernetes cluster’s location.',
    ),

    tags=dict(
        type='list',
        elements='str',
        description='An array of tags applied to the Kubernetes cluster.',
    ),

    node_pools=dict(
        type='list',
        elements='dict',
        suboptions=linode_lke_cluster_node_pool_spec,
        description='A list of node pools to configure the cluster with'
    ),

    skip_polling=dict(
        type='bool',
        description='If true, the module will not wait for all nodes in the cluster to be ready.',
        default=False
    ),

    wait_timeout=dict(
        type='int',
        description='The period to wait for the cluster to be ready in seconds.',
        default=600
    )
)

specdoc_meta = dict(
    description=[
        'Manage Linode LKE clusters.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_lke_cluster_spec,
    examples=docs.examples,
    return_values=dict(
        cluster=dict(
            description='The LKE cluster in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/linode-kubernetes-engine-lke/'
                     '#kubernetes-cluster-view__response-samples',
            type='dict',
            sample=docs.result_cluster
        ),
        node_pools=dict(
            description='A list of node pools in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/linode-kubernetes-engine-lke/'
                     '#node-pools-list__response-samples',
            type='list',
            sample=docs.result_node_pools
        ),
        kubeconfig=dict(
            description=[
                'The Base64-encoded kubeconfig used to access this cluster.',
                'NOTE: This value may be unavailable if `skip_polling` is true.'
            ],
            docs_url='https://www.linode.com/docs/api/linode-kubernetes-engine-lke/' \
                     '#kubeconfig-view__responses',
            type='str'
        ),
        dashboard_url=dict(
            description='The Cluster Dashboard access URL.',
            docs_url='https://www.linode.com/docs/api/linode-kubernetes-engine-lke/'
                     '#kubernetes-cluster-dashboard-url-view__responses',
            type='str'
        )
    )
)

MUTABLE_FIELDS: Set[str] = {
    'tags'
}

REQUIRED_PRESENT: Set[str] = {
    'k8s_version',
    'region',
    'label',
    'node_pools'
}


class LinodeLKECluster(LinodeModuleBase):
    """Module for creating and destroying Linode LKE clusters"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_lke_cluster_spec
        self.required_one_of: List[str] = []
        self.results = dict(
            changed=False,
            actions=[],
            cluster=None,
            node_pools=None,
            dashboard_url=None,
            kubeconfig=None
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

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
            return self.fail(msg='failed to get lke cluster {0}: {1}'.format(name, exception))

    def _wait_for_all_nodes_ready(self, cluster: LKECluster, timeout: int) -> None:
        def _check_cluster_nodes_ready() -> bool:
            for pool in cluster.pools:
                for node in pool.nodes:
                    if node.status != 'ready':
                        return False
            return True

        try:
            polling.poll(
                _check_cluster_nodes_ready,
                step=4,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail('failed to wait for lke cluster: timeout period expired')

    def _create_cluster(self) -> Optional[LKECluster]:
        params = copy.deepcopy(self.module.params)
        label = params.pop('label')
        region = params.pop('region')
        node_pools = params.pop('node_pools')
        kube_version = params.pop('k8s_version')
        params = filter_null_values(params)

        try:
            self.register_action('Created LKE cluster {0}'.format(label))
            return self.client.lke.cluster_create(region, label, node_pools, kube_version, **params)
        except Exception as exception:
            return self.fail(msg='failed to create lke cluster: {0}'.format(exception))

    def _update_cluster(self, cluster: LKECluster) -> None:
        """Handles all update functionality for the current LKE cluster"""

        new_params = copy.deepcopy(self.module.params)
        pools = new_params.pop('node_pools')
        k8s_version = new_params.pop('k8s_version')

        handle_updates(cluster, new_params, MUTABLE_FIELDS, self.register_action)

        # version upgrade
        if cluster.k8s_version.id != k8s_version:
            self.client.put('/lke/clusters/{}'.format(cluster.id), data={
                'k8s_version': k8s_version
            })

            self.register_action('Upgraded cluster {} -> {}'.
                                 format(cluster.k8s_version.id, k8s_version))

        existing_pools = copy.deepcopy(cluster.pools)
        should_keep = [False for _ in existing_pools]
        pools_handled = [False for _ in pools]

        for k, pool in enumerate(pools):
            for i, current_pool in enumerate(existing_pools):
                if should_keep[i]:
                    continue

                # pool already exists
                if current_pool.count == pool['count'] and current_pool.type.id == pool['type']:
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

                if existing_pool.type.id == pool['type']:
                    self.register_action('Resized pool {} from {} -> {}'.
                                         format(existing_pool.id,
                                                existing_pool.count, pool['count']))
                    existing_pool.count = pool['count']
                    existing_pool.save()
                    should_keep[k] = True

                    created = True
                    break

            if not created:
                self.register_action('Created pool with {} nodes and type {}'
                                     .format(pool['count'], pool['type']))
                cluster.node_pool_create(pool['type'], pool['count'])

        for i, pool in enumerate(existing_pools):
            if should_keep[i]:
                continue

            self.register_action('Deleted pool {}'.format(pool.id))
            pool.delete()

    def _populate_kubeconfig(self, cluster: LKECluster) -> None:
        if self.module.params.get('skip_polling'):
            try:
                self.results['kubeconfig'] = cluster.kubeconfig
            except ApiError as error:
                if error.status != 503:
                    self.fail(error)

                self.results['kubeconfig'] = 'Kubeconfig not yet available...'
            except Exception as exception:
                self.fail(exception)
            return

        def _try_get_kubeconfig() -> bool:
            try:
                self.results['kubeconfig'] = cluster.kubeconfig
            except ApiError as error:
                if error.status != 503:
                    self.fail(error)

                return False
            except Exception as exception:
                self.fail(exception)

            return True

        try:
            polling.poll(
                _try_get_kubeconfig,
                step=4,
                timeout=self.module.params.get('wait_timeout'),
            )
        except polling.TimeoutException:
            self.fail('failed to wait for lke cluster kubeconfig: timeout period expired')

    def _populate_results(self, cluster: LKECluster) -> None:
        cluster._api_get()
        dashboard_data = self.client.get('/lke/clusters/{}/dashboard'.format(cluster.id))

        self.results['cluster'] = cluster._raw_json
        self.results['node_pools'] = [jsonify_node_pool(pool) for pool in cluster.pools]
        self.results['dashboard_url'] = dashboard_data['url']

        self._populate_kubeconfig(cluster)

    def _handle_present(self) -> None:
        params = self.module.params

        try:
            validate_required(REQUIRED_PRESENT, params)
        except Exception as exception:
            self.fail(exception)

        label: str = params.get('label')

        cluster = self._get_cluster_by_name(label)

        # Create the domain if it does not already exist
        if cluster is None:
            cluster = self._create_cluster()

        self._update_cluster(cluster)

        # Force lazy-loading
        cluster._api_get()

        if not params.get('skip_polling'):
            self._wait_for_all_nodes_ready(cluster, params.get('wait_timeout'))

        self._populate_results(cluster)

    def _handle_absent(self) -> None:
        label: str = self.module.params.get('label')

        cluster = self._get_cluster_by_name(label)

        if cluster is not None:
            self._populate_results(cluster)

            cluster.delete()
            self.register_action('Deleted cluster {0}'.format(cluster))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Domain module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeLKECluster()


if __name__ == '__main__':
    main()
