#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode LKE Types."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_type_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="LKE Types",
    result_field_name="lke_types",
    endpoint_template="/lke/types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_lke_type_samples,
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
