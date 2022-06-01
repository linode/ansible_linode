#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
from typing import Optional, cast, Any, Set, List, Dict

from linode_api4 import LKECluster, LKENodePool

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    filter_null_values, paginated_list_to_json, jsonify_node_pool
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain as docs

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
    )

)

specdoc_meta = dict(
    description=[
        'Manage Linode LKE clusters.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_lke_cluster_spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        domain=dict(
            description='The domain in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/domains/#domain-view',
            type='dict',
            sample=docs.result_domain_samples
        ),
        records=dict(
            description='The domain record in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/domains/#domain-record-view',
            type='list',
            sample=docs.result_records_samples
        )
    )
)

MUTABLE_FIELDS: Set[str] = {
    'tags',
    'high_availability'
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

        handle_updates(cluster, new_params, MUTABLE_FIELDS, self.register_action)

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

            # if not exists:
            #     self.register_action('Created pool with {} nodes and type {}'.format(pool['count'], pool['type']))
            #     cluster.node_pool_create(pool['type'], pool['count'])

        for i, pool in enumerate(pools):
            if pools_handled[i]:
                continue

            created = False

            for k, existing_pool in enumerate(existing_pools):
                if should_keep[k]:
                    continue

                if existing_pool.type.id == pool['type']:
                    self.register_action('Resized pool {} from {} -> {}'.format(existing_pool.id, existing_pool.count, pool['count']))
                    existing_pool.count = pool['count']
                    existing_pool.save()
                    should_keep[k] = True

                    created = True
                    break

            if not created:
                self.register_action('Created pool with {} nodes and type {}'.format(pool['count'], pool['type']))
                cluster.node_pool_create(pool['type'], pool['count'])

        for i, pool in enumerate(existing_pools):
            if should_keep[i]:
                continue

            self.register_action('Deleted pool {}'.format(pool.id))
            pool.delete()

    def _handle_present(self) -> None:
        params = self.module.params

        label: str = params.get('label')

        cluster = self._get_cluster_by_name(label)

        # Create the domain if it does not already exist
        if cluster is None:
            cluster = self._create_cluster()

        self._update_cluster(cluster)

        # Force lazy-loading
        cluster._api_get()

        self.results['cluster'] = cluster._raw_json
        self.results['node_pools'] = [jsonify_node_pool(pool) for pool in cluster.pools]

    def _handle_absent(self) -> None:
        label: str = self.module.params.get('label')

        cluster = self._get_cluster_by_name(label)

        if cluster is not None:
            self.results['cluster'] = cluster._raw_json
            self.results['node_pools'] = [jsonify_node_pool(pool) for pool in cluster.pools]

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
