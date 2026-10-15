#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for listing Monitor Logs Stream quotas."""

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    monitor_logs_stream_quota_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Monitor Logs Stream Quotas",
    result_field_name="stream_quotas",
    endpoint_template="/monitor/streams/quotas",
    result_docs_url="TODO",
    examples=docs.specdoc_examples,
    result_samples=docs.result_stream_quotas_samples,
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
