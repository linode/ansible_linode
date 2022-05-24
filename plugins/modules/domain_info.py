#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import List, Any, Optional

from linode_api4 import Domain

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import create_filter_and, \
    paginated_list_to_json
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

from ansible_collections.linode.cloud.plugins.modules.domain import specdoc_meta \
    as domain_specdoc_meta

linode_domain_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False, doc_hide=True),
    label=dict(type='str', required=False, doc_hide=True),

    id=dict(type='int', required=False,
            description='The unique domain name of the Domain.'),
    domain=dict(type='str', required=False,
                description='The unique id of the Domain.')
)

specdoc_examples = ['''
- name: Get info about a domain by domain
  linode.cloud.domain_info:
    domain: my-domain.com''', '''
- name: Get info about a domain by id
  linode.cloud.domain_info:
    id: 12345''']

result_domain_samples = ['''{
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

result_records_samples = ['''[
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

specdoc_meta = dict(
    description=[
        'Get info about a Linode Domain.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_domain_info_spec,
    examples=specdoc_examples,
    return_values=domain_specdoc_meta['return_values']
)

linode_domain_valid_filters = [
    'id', 'domain'
]


class LinodeDomainInfo(LinodeModuleBase):
    """Module for getting info about a Linode Domain"""

    def __init__(self) -> None:
        self.module_arg_spec = linode_domain_info_spec
        self.required_one_of: List[str] = []
        self.results = dict(
            domain=None,
            records=None
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def _get_matching_domain(self, spec_args: dict) -> Optional[Domain]:
        filter_items = {k: v for k, v in spec_args.items()
                        if k in linode_domain_valid_filters and v is not None}

        filter_statement = create_filter_and(Domain, filter_items)

        try:
            # Special case because ID is not filterable
            if 'id' in filter_items.keys():
                result = Domain(self.client, spec_args.get('id'))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.domains(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg='failed to get domain {0}'.format(exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for domain info module"""

        domain = self._get_matching_domain(kwargs)

        if domain is None:
            self.fail('failed to get domain')

        self.results['domain'] = domain._raw_json
        self.results['records'] = paginated_list_to_json(domain.records)

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain info module"""
    LinodeDomainInfo()


if __name__ == '__main__':
    main()
