#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode instance types. Deprecated in favor of type_list."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    instance_type_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Instance Types",
    result_field_name="instance_types",
    endpoint_template="/linode/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_instance_type_samples,
    deprecated=True,
    deprecation_message="This module has been deprecated in favor of `type_list`.",
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
