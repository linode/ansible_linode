#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Object Storage clusters. ."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_cluster_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Object Storage Clusters",
    result_field_name="clusters",
    endpoint_template="/object-storage/clusters",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-clusters",
    result_samples=docs.result_object_clusters_samples,
    examples=docs.specdoc_examples,
    deprecated=True,
    deprecation_message="This module has been deprecated because it "
    + "relies on deprecated API endpoints. Going forward, `region` will "
    + "be the preferred way to designate where Object Storage resources "
    + "should be created.",
)

SPECDOC_META = module.spec

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

if __name__ == "__main__":
    module.run()
