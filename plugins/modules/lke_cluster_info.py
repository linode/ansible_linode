#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Volumes."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional, Dict

from linode_api4 import LKECluster, LKENodePool

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and,\
    jsonify_node_pool, filter_null_values
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_cluster \
    as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_cluster_info as docs

linode_lke_cluster_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False, doc_hide=True),

    id=dict(
        type='int', required=False,
        description=[
            'The ID of the LKE cluster.',
            'Optional if `label` is defined.'
        ]),

    label=dict(
        type='str', required=False,
        description=[
            'The label of the LKE cluster.',
            'Optional if `id` is defined.'
        ])
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode LKE cluster.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_lke_cluster_info_spec,
    examples=docs.examples,
    return_values=dict(
        cluster=dict(
            description='The LKE cluster in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/linode-kubernetes-engine-lke/'
                     '#kubernetes-cluster-view__response-samples',
            type='dict',
            sample=docs_parent.result_cluster
        ),
        node_pools=dict(
            description='A list of node pools in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/linode-kubernetes-engine-lke/'
                     '#node-pools-list__response-samples',
            type='list',
            sample=docs_parent.result_node_pools
        )
    )
)

VALID_FILTERS = [
    'id', 'label'
]


class LinodeLKEClusterInfo(LinodeModuleBase):
    """Module for getting info about a Linode Volume"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_lke_cluster_info_spec
        self.required_one_of: List[str] = []
        self.results: Dict[str, Any] = dict(
            cluster=None,
            node_pools=[],
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

    def _get_cluster_from_kwargs(self, **kwargs: Any) -> LKECluster:
        args = filter_null_values(kwargs)

        if 'id' in args:
            cluster = LKECluster(self.client, args.get('id'))
            cluster._api_get()
            return cluster

        if 'label' in args:
            return self._get_cluster_by_name(args.get('label'))

        return self.fail(msg='one of `label` or `id` must be specified')

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for LKE cluster info module"""

        cluster = self._get_cluster_from_kwargs(**kwargs)

        if cluster is None:
            self.fail('failed to get cluster')

        self.results['cluster'] = cluster._raw_json
        self.results['node_pools'] = [jsonify_node_pool(pool) for pool in cluster.pools]

        return self.results


def main() -> None:
    """Constructs and calls the Linode Volume info module"""
    LinodeLKEClusterInfo()


if __name__ == '__main__':
    main()
