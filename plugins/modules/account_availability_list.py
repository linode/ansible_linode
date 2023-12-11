#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Account Availabilities."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    account_availability_list as docs
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Account Availability",
    result_field_name="account_availabilities",
    endpoint_template="/account/availability",
    result_docs_url="TBD",
    result_samples=docs.result_account_availabilities_samples,
    examples=docs.specdoc_examples,
)

SPECDOC_META = module.spec

if __name__ == "__main__":
    module.run()
