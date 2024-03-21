#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for listing Linode Account Children."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    child_account_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Child Account",
    result_field_name="child_accounts",
    endpoint_template="/account/child-accounts",
    result_docs_url="",
    examples=docs.specdoc_examples,
    result_samples=docs.result_child_accounts_samples,
)

SPECDOC_META = module.spec

if __name__ == "__main__":
    module.run()
