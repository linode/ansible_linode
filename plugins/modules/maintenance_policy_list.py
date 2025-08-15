#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Maintenance Policies.
"NOTE: This module is under v4beta.","""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    maintenance_policy_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Maintenance Policies",
    result_field_name="maintenance_policies",
    endpoint_template="/maintenance/policies",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-policies",
    examples=docs.specdoc_examples,
    result_samples=docs.result_maintenance_policy_samples,
    requires_beta=True,
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
