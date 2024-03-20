#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage Cluster info."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_cluster_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ObjectStorageCluster, Region

linode_object_cluster_info_spec = {
    "api_token": SpecField(
        type=FieldType.string,
        required=False,
        description="The Linode account personal access token. "
        "It is necessary to run the module. "
        "It can be exposed by the "
        "environment variable `LINODE_API_TOKEN` instead.",
    ),
    # We need to overwrite attributes to exclude them as requirements
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.string,
        required=False,
        description=["The unique id given to the clusters."],
    ),
    "region": SpecField(
        type=FieldType.string,
        required=False,
        description=["The region the clusters are in."],
    ),
    "domain": SpecField(
        type=FieldType.string,
        required=False,
        description=["The domain of the clusters."],
    ),
    "static_site_domain": SpecField(
        type=FieldType.string,
        required=False,
        description=["The static-site domain of the clusters."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode Object Storage Cluster."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_object_cluster_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "clusters": SpecReturnValue(
            description="The Object Storage clusters in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/object-storage/#cluster-view__responses",
            type=FieldType.list,
            sample=docs.result_clusters_samples,
        )
    },
)

FILTERABLE_FIELDS = [
    "id",
    "region",
    "domain",
    "static_site_domain",
]


class LinodeObjectStorageClustersInfo(LinodeModuleBase):
    """Module for getting info about a Linode Object Storage Cluster"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {"changed": False, "actions": [], "clusters": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _cluster_matches_filter(self, cluster: ObjectStorageCluster) -> bool:
        for k in FILTERABLE_FIELDS:
            user_input = self.module.params.get(k)
            if user_input is None:
                continue

            cluster_value = getattr(cluster, k)

            # This is necessary because regions are populated as
            # Region objects by linode_api4.
            if isinstance(cluster_value, Region):
                cluster_value = cluster_value.id

            if cluster_value != user_input:
                return False

        return True

    def _get_matching_clusters(self) -> Optional[List[ObjectStorageCluster]]:
        try:
            return [
                v
                for v in self.client.object_storage.clusters()
                if self._cluster_matches_filter(v)
            ]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg="failed to get clusters {0}".format(exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Constructs and calls the Linode Object Storage Clusters module"""

        clusters = self._get_matching_clusters()

        if clusters is None:
            return self.fail("failed to get clusters")

        self.results["clusters"] = [cluster._raw_json for cluster in clusters]

        return self.results


def main() -> None:
    """Constructs and calls the Linode Object Storage Clusters module"""

    LinodeObjectStorageClustersInfo()


if __name__ == "__main__":
    main()
