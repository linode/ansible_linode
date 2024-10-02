#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Volume Types."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.volume_type_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Volume Types",
    result_field_name="volume_types",
    endpoint_template="/volumes/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-volume-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_volume_type_samples,
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
