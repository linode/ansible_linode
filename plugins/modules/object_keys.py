#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage keys."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from linode_api4 import ObjectStorageKeys, ObjectStorageCluster

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
module: object_keys
description: Manage Linode Object Storage Keys.
requirements:
  - python >= 2.7
  - linode_api4 >= 3.0
author:
  - Luke Murphy (@decentral1se)
  - Charles Kenney (@charliekenney23)
  - Phillip Campbell (@phillc)
  - Lena Garber (@lbgarber)
options:
  label:
    description:
      - The unique label to give this key
    required: true
    type: string
  access:
    description:
      - A list of access permissions to give the key.
    required: false
    type: list
    elements: dict
    suboptions:
      cluster:
        description:
          - The id of the cluster that the provided bucket exists under.
        type: str
        required: true
      bucket_name:
        description:
          - The name of the bucket to set the key's permissions for.
        type: str
        required: true
      permissions:
        description:
          - The permissions to give the key.
        type: str
        required: true
        choices:
          - read_only
          - write_only
          - read_write
'''

EXAMPLES = '''
- name: Create an Object Storage key
  linode.cloud.object_keys:
    label: 'my-fullaccess-key'
    state: present
    
- name: Create a limited Object Storage key
  linode.cloud.object_keys:
    label: 'my-limited-key'
    access:
      - cluster: us-east-1
        bucket_name: my-bucket
        permissions: read_write
    state: present
    
- name: Remove an object storage key
  linode.cloud.object_keys:
    label: 'my-key'
    state: absent
'''

RETURN = '''
key:
  description: The Object Storage key in JSON serialized form.
  returned: Always.
  type: dict
  sample: {
   "access_key":"xxxxxxxxxxxxxxxxx",
   "bucket_access":[
      {
         "bucket_name":"my-bucket",
         "cluster":"us-east-1",
         "permissions":"read_write"
      }
   ],
   "id":xxxxx,
   "label":"my-key",
   "limited":true,
   "secret_key":"xxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
'''

linode_access_spec = dict(
    cluster=dict(type='str', required=True),
    bucket_name=dict(type='str', required=True),
    permissions=dict(type='str', required=True)
)

linode_object_keys_spec = dict(
    access=dict(type='list', required=False, elements='dict', options=linode_access_spec)
)


class LinodeObjectStorageKeys(LinodeModuleBase):
    """Configuration class for Linode Object Storage Keys resource"""

    def __init__(self):
        self.module_arg_spec = linode_object_keys_spec
        self.required_one_of = ['state', 'label']
        self.results = dict(
            changed=False,
            actions=[],
            key=None,
        )

        self._key = None

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def get_key_by_label(self, label):
        """Gets the Object Storage key with the given label"""

        try:
            # For some reason we can't filter on label here
            keys = self.client.object_storage.keys()

            key = None
            for current_key in keys:
                if current_key.label == label:
                    key = current_key

            return key

        except IndexError:
            return None
        except Exception as exception:
            self.fail(msg='failed to get object storage key {0}: {1}'.format(label, exception))

    def create_key(self, label, bucket_access):
        """Creates an Object Storage key with the given label and access"""

        try:
            return self.client.object_storage.keys_create(label, bucket_access=bucket_access)
        except Exception as exception:
            self.fail(msg='failed to create object storage key: {0}'.format(exception))

    def _dict_to_bucket_access(self, access_items):
        "Converts the given bucket_access spec items into an API compliant format"

        return [self.client.object_storage.bucket_access(
            v.get('cluster'),
            v.get('bucket'),
            v.get('permissions')
        ) for v in access_items]

    def __handle_key(self, **kwargs):
        """Updates the key defined in kwargs"""

        label = kwargs.pop('label')

        self._key = self.get_key_by_label(label)

        if self._key is None:
            self._key = self.create_key(label, bucket_access=kwargs.get('access'))
            self.register_action('Created key {0}'.format(label))

        self.results['key'] = self._key._raw_json

    def __handle_key_absent(self, **kwargs):
        """Deletes the key defined in kwargs"""

        label = kwargs.pop('label')

        self._key = self.get_key_by_label(label)

        if self._key is not None:
            self.results['key'] = self._key._raw_json
            self._key.delete()
            self.register_action('Deleted key {0}'.format(label))


    def exec_module(self, **kwargs):
        """Constructs and calls the Linode Object Storage Key module"""

        state = kwargs.pop('state')

        if state == 'absent':
            self.__handle_key_absent(**kwargs)
            return self.results

        self.__handle_key(**kwargs)

        return self.results

def main():
    """Constructs and calls the Linode Object Storage key module"""
    LinodeObjectStorageKeys()


if __name__ == '__main__':
    main()
