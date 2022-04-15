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

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'Linode'
}

DOCUMENTATION = '''
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)
description:
- Get info about a Linode Domain.
module: domain_info
options:
  domain:
    description: The unique id of the Domain.
    required: false
    type: str
  id:
    description: The unique domain name of the Domain.
    required: false
    type: int
requirements:
- python >= 3
'''

EXAMPLES = '''
- name: Get info about a domain by domain
  linode.cloud.domain_info:
    domain: my-domain.com

- name: Get info about a domain by id
  linode.cloud.domain_info:
    id: 12345
'''

RETURN = '''
domain:
  description: The domain in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/domains/#domain-view"
  returned: always
  type: dict
  sample: {
   "axfr_ips":[],
   "created":"xxxx",
   "description":"Created with ansible!",
   "domain":"my-domain.com",
   "expire_sec":300,
   "group":"",
   "id":xxxxxx,
   "master_ips":[
      "127.0.0.1"
   ],
   "refresh_sec":3600,
   "retry_sec":7200,
   "soa_email":"xxxx@my-domain.com",
   "status":"active",
   "tags":[],
   "ttl_sec":14400,
   "type":"master",
   "updated":"xxxx"
}

records:
  description: A list of records associated with the domain in JSON serialized form.
  linode_api_docs: "https://www.linode.com/docs/api/domains/#domain-record-view"
  returned: always
  type: list
  sample: [{
   "created":"xxxxx",
   "id":xxxxx,
   "name":"xxxx",
   "port":0,
   "priority":0,
   "protocol":null,
   "service":null,
   "tag":null,
   "target":"127.0.0.1",
   "ttl_sec":3600,
   "type":"A",
   "updated":"xxxxx",
   "weight":55
}]
'''

linode_domain_info_spec = dict(
    # We need to overwrite attributes to exclude them as requirements
    state=dict(type='str', required=False, doc_hide=True),
    label=dict(type='str', required=False, doc_hide=True),

    id=dict(type='int', required=False,
            description='The unique domain name of the Domain.'),
    domain=dict(type='str', required=False,
                description='The unique id of the Domain.')
)

specdoc_meta = dict(
    description=[
        'Get info about a Linode Domain.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=linode_domain_info_spec
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
