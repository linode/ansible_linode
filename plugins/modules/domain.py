#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import Optional, cast, Any, Set, List

from linode_api4 import Domain

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    filter_null_values, paginated_list_to_json
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

linode_domain_spec = dict(
    # Unused for domain objects
    label=dict(type='str', required=False, doc_hide=True),

    axfr_ips=dict(type='list', elements='str',
                  description='The list of IPs that may perform a zone transfer for this Domain.'),
    description=dict(type='str',
                     description='The list of IPs that may perform a '
                                 'zone transfer for this Domain.'),
    domain=dict(type='str', required=True,
                description='The domain this Domain represents.'),
    expire_sec=dict(type='int',
                    description='The amount of time in seconds that may pass'
                                ' before this Domain is no longer authoritative.'),
    master_ips=dict(type='list', elements='str',
                    description='The IP addresses representing the '
                                'master DNS for this Domain.'),
    refresh_sec=dict(type='int',
                     description='The amount of time in seconds before '
                                 'this Domain should be refreshed.'),
    retry_sec=dict(type='int',
                   description='The interval, in seconds, at which a '
                               'failed refresh should be retried.'),
    soa_email=dict(type='str',
                   description='The Start of Authority email address.'),
    status=dict(type='str',
                description='Used to control whether this Domain is currently being rendered.'),
    tags=dict(type='list', elements='str',
              description='An array of tags applied to this object.'),
    ttl_sec=dict(type='int',
                 description='the amount of time in seconds that this '
                             'Domain’s records may be cached by resolvers '
                             'or other domain servers.'),
    type=dict(type='str',
              description='Whether this Domain represents the authoritative '
                          'source of information for the domain'
                          ' it describes (master), or whether it is a '
                          'read-only copy of a master (slave).'),

    # Deprecated
    group=dict(type='str', doc_hide=True)
)

specdoc_meta = dict(
    description=[
        'Manage Linode Domains.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_domain_spec,
    examples=['''
- name: Create a domain 
  linode.cloud.domain:
    domain: my-domain.com
    type: master
    state: present

- name: Delete a domain
  linode.cloud.domain:
    domain: my-domain.com
    state: absent'''],
    return_values=dict(
        domain=dict(
            description='The domain in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/domains/#domain-view',
            type='dict',
            sample=['''
{
  "axfr_ips": [],
  "description": null,
  "domain": "example.org",
  "expire_sec": 300,
  "group": null,
  "id": 1234,
  "master_ips": [],
  "refresh_sec": 300,
  "retry_sec": 300,
  "soa_email": "admin@example.org",
  "status": "active",
  "tags": [
    "example tag",
    "another example"
  ],
  "ttl_sec": 300,
  "type": "master"
}''']
        ),
        records=dict(
            description='The domain record in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/domains/#domain-record-view',
            type='list',
            sample=['''[
  {
    "created": "2018-01-01T00:01:01",
    "id": 123456,
    "name": "test",
    "port": 80,
    "priority": 50,
    "protocol": null,
    "service": null,
    "tag": null,
    "target": "192.0.2.0",
    "ttl_sec": 604800,
    "type": "A",
    "updated": "2018-01-01T00:01:01",
    "weight": 50
  }
]''']
        )
    )
)

linode_domain_mutable: Set[str] = {
    'axfr_ips',
    'description',
    'expire_sec',
    'master_ips',
    'refresh_sec',
    'retry_sec',
    'soa_email',
    'status',
    'tags',
    'ttl_sec',
    'type',
    'group'
}


class LinodeDomain(LinodeModuleBase):
    """Module for creating and destroying Linode Domains"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_domain_spec
        self.required_one_of: List[str] = []
        self.results = dict(
            changed=False,
            actions=[],
            domain=None,
        )

        self._domain: Optional[Domain] = None

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def _get_domain_by_name(self, name: str) -> Optional[Domain]:
        try:
            domain = self.client.domains(Domain.domain == name)[0]

            # Fix for group returning '' rather than None
            if domain.group == '':
                domain.group = None

            return domain
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get domain {0}: {1}'.format(name, exception))

    def _create_domain(self) -> Optional[Domain]:
        params = self.module.params
        domain = params.pop('domain')
        master = params.pop('type') == 'master'

        try:
            self.register_action('Created domain {0}'.format(domain))
            return self.client.domain_create(domain, master, **params)
        except Exception as exception:
            return self.fail(msg='failed to create domain: {0}'.format(exception))

    def _update_domain(self) -> None:
        """Handles all update functionality for the current Domain"""

        # Update mutable values
        should_update = False
        params = filter_null_values(self.module.params)

        for key, new_value in params.items():
            if not hasattr(self._domain, key):
                continue

            old_value = getattr(self._domain, key)

            if new_value != old_value:
                if key in linode_domain_mutable:
                    setattr(self._domain, key, new_value)
                    self.register_action('Updated Domain {0}: "{1}" -> "{2}"'.
                                         format(key, old_value, new_value))

                    should_update = True
                    continue

                self.fail(
                    'failed to update domain {0}: {1} is a non-updatable field'
                        .format(self._domain.domain, key))

        if should_update:
            self._domain.save()

    def _handle_domain(self) -> None:
        params = self.module.params

        domain_name: str = params.get('domain')

        self._domain = self._get_domain_by_name(domain_name)

        # Create the domain if it does not already exist
        if self._domain is None:
            self._domain = self._create_domain()

        self._update_domain()

        # Force lazy-loading
        self._domain._api_get()

        self.results['domain'] = self._domain._raw_json
        self.results['records'] = paginated_list_to_json(self._domain.records)

    def _handle_domain_absent(self) -> None:
        domain_name: str = self.module.params.get('domain')

        self._domain = self._get_domain_by_name(domain_name)

        if self._domain is not None:
            self.results['domain'] = self._domain._raw_json
            self.results['records'] = paginated_list_to_json(self._domain.records)

            self._domain.delete()
            self.register_action('Deleted domain {0}'.format(domain_name))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Domain module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_domain_absent()
            return self.results

        self._handle_domain()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeDomain()


if __name__ == '__main__':
    main()
