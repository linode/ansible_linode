#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage Cluster info."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from linode_api4 import ObjectStorageKeys, ObjectStorageCluster

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
module: object_cluster_info
description: Get information about an Object Storage cluster.
requirements:
  - python >= 2.7
  - linode_api4 >= 3.0
author:
  - Luke Murphy (@decentral1se)
  - Charles Kenney (@charliekenney23)
  - Phillip Campbell (@phillc)
  - Lena Garber (@lbgarber)
options:
  id:
    description:
      - The unique id given to the clusters
    type: string
  region:
    description:
      - The region the clusters are in
    type: string
  domain:
    description:
      - The domain of the clusters
    type: string
  static_site_domain:
    description:
      - The static-site domain of the clusters
    type: string
'''

EXAMPLES = '''
- name: Get info about clusters in us-east
  linode.cloud.object_cluster_info:
    region: us-east

- name: Get info about the cluster with id us-east-1
  linode.cloud.object_cluster_info:
    id: us-east-1
'''

RETURN = '''
clusters:
  description: The Object Storage clusters in JSON serialized form.
  returned: Always.
  type: list
  elements: dict
  sample: [
   {
      "domain":"us-east-1.linodeobjects.com",
      "id":"us-east-1",
      "region":"us-east",
      "static_site_domain":"website-us-east-1.linodeobjects.com",
      "status":"available"
   }
]
'''

linode_object_cluster_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False),
    label=dict(type='str', required=False),

    id=dict(type='str', required=False),
    region=dict(type='str', required=False),
    domain=dict(type='str', required=False),
    static_site_domain=dict(type='str', required=False)
)

linode_object_cluster_valid_filters = [
    'id', 'region', 'domain', 'static_site_domain'
]


class LinodeObjectStorageClustersInfo(LinodeModuleBase):
    """Configuration class for Linode Object Storage Clusters resource"""

    def __init__(self):
        self.module_arg_spec = linode_object_cluster_info_spec
        self.required_one_of = []
        self.results = dict(
            changed=False,
            actions=[],
            clusters=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def get_clusters_by_property(self, **kwargs):
        """Gets a list of clusters with the given property in kwargs"""

        filter_items = {k: v for k, v in kwargs.items()
                        if k in linode_object_cluster_valid_filters and v is not None}

        filter_statement = create_filter_and(ObjectStorageCluster, filter_items)

        try:
            # Special case because ID is not filterable
            if 'id' in filter_items.keys():
                result = ObjectStorageCluster(self.client, kwargs.get('id'))
                result._api_get()  # Force lazy-loading

                return [result]

            return self.client.object_storage.clusters(filter_statement)
        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get clusters {0}'.format(exception))


    def exec_module(self, **kwargs):
        """Constructs and calls the Linode Object Storage Clusters module"""

        clusters = self.get_clusters_by_property(**kwargs)

        if clusters is None:
            self.fail('failed to get clusters')

        self.results['clusters'] = [cluster._raw_json for cluster in clusters]

        return self.results

def main():
    """Constructs and calls the Linode Object Storage Clusters module"""
    LinodeObjectStorageClustersInfo()


if __name__ == '__main__':
    main()
