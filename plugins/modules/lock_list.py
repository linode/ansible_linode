#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode resource locks."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lock_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Locks",
    result_field_name="locks",
    endpoint_template="/locks",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-resource-locks",
    examples=docs.specdoc_examples,
    result_samples=docs.result_locks_samples,
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
