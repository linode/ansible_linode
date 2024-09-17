#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode LKE Versions."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    lke_version_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="LKE Versions",
    result_field_name="lke_versions",
    endpoint_template="/lke/versions",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-versions",
    result_samples=docs.result_lke_versions_samples,
    examples=docs.specdoc_examples,
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
