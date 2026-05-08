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
    api_filter_constructor_for_aclp_monitor_services,
)


def api_filter_for_logs_destination_services(
    params: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Customize a filter string for listing Logs Destinations,
    because on the API side nested filter operators are not supported.
    Contrary to C(api_filter_constructor_for_aclp_monitor_services), `order_by` and `order` are supported.
    Converts 'id' strings to integers to meet type requirements for the Logs Destination API.
    """
    filters = params.get("filters")
    if filters:
        for f in filters:
            if f.get("name") == "id":
                f["values"] = [
                    int(v) if isinstance(v, str) and v.isdigit() else v
                    for v in f["values"]
                ]
    value_filters = api_filter_constructor_for_aclp_monitor_services(params)
    order_by = params.get("order_by")
    order = params.get("order")
    if order_by:
        value_filters["+order_by"] = order_by
        if order:
            value_filters["+order"] = order

    return value_filters


module = ListModule(
    result_display_name="Logs Destinations",
    result_field_name="logs_destinations",
    endpoint_template="/monitor/streams/destinations",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-destinations",
    examples=docs.specdoc_examples,
    result_samples=docs.result_logs_destinations_samples,
    custom_api_filter_constructor=api_filter_for_logs_destination_services,
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
