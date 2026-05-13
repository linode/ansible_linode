#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    logs_destination_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    api_filter_for_aclp_logs_services,
)


module = ListModule(
    result_display_name="Logs Destinations",
    result_field_name="logs_destinations",
    endpoint_template="/monitor/streams/destinations",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-destinations",
    examples=docs.specdoc_examples,
    result_samples=docs.result_logs_destinations_samples,
    custom_api_filter_constructor=api_filter_for_aclp_logs_services,
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
