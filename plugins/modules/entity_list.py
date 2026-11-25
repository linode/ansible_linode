#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list the entities of their account."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    entity_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Entities",
    result_field_name="entities",
    endpoint_template="/entities",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-entities",
    examples=docs.specdoc_examples,
    result_samples=docs.result_entities_samples,
    requires_beta=True,
    disable_filters=True,
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
