#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for listing
history of a ACLP Monitor Service Logs Destination."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    monitor_logs_destination_history as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    api_filter_for_aclp_logs_services,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="Logs Destination History",
    result_field_name="logs_destination_history",
    endpoint_template="/monitor/streams/destinations/{id}/history",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-destination-history",
    examples=docs.specdoc_examples,
    result_samples=docs.result_logs_destination_history_samples,
    custom_api_filter_constructor=api_filter_for_aclp_logs_services,
    params=[
        ListModuleParam(
            display_name="ID",
            name="id",
            type=FieldType.integer,
        ),
    ],
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
