#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Maintenance Policies."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.maintenance_policy_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Maintenance Policies",
    result_field_name="maintenance_policies",
    endpoint_template="/maintenance/policies",
    # TODO result_docs_url="",
    examples=docs.specdoc_examples,
    result_samples=docs.result_maintenance_policy_samples,
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
