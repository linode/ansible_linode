#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for listing Linode Monitor Logs Streams."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    monitor_logs_stream_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    api_filter_for_aclp_logs_services,
)

module = ListModule(
    result_display_name="Monitor Logs Streams",
    result_field_name="streams",
    endpoint_template="/monitor/streams",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-streams",
    examples=docs.specdoc_examples,
    result_samples=docs.result_streams_samples,
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
