#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Placement Groups."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    placement_group_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Placement Groups",
    result_field_name="placement_groups",
    endpoint_template="/placement/groups",
    result_docs_url="TBD",
    result_samples=docs.result_placement_groups_samples,
    examples=docs.specdoc_examples,
    requires_beta=True,
)

SPECDOC_META = module.spec

DOCUMENTATION = '''
'''
EXAMPLES = '''
'''
RETURN = '''
'''

if __name__ == "__main__":
    module.run()
