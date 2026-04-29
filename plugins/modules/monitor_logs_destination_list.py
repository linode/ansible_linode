from __future__ import absolute_import, division, print_function

from typing import Any, Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    logs_destinations_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    api_filter_constructor_for_aclp_monitor_services,
)


def custom_api_filter_constructor(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    fixme rename, should we leave custom constructor?
    Customize a filter string for listing Monitor Service Alert Definitions,
    because on the API side only the `+and` and `+or` operators are supported,
    and you can't nest filter operators.
    """
    if params.get("order_by") is not None or params.get("order") is not None:
        module.warn(
            "order or order_by is currently not supported in "
            "listing the alert definitions, "
            "and will be ignored if provided. "
            "Please refer to the API documentation for more information."
        )

    return api_filter_constructor_for_aclp_monitor_services(params)


module = ListModule(
    result_display_name="Logs Destinations",
    result_field_name="logs_destinations",
    endpoint_template="/monitor/streams/destinations",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-destinations",
    examples=docs.specdoc_examples,
    result_samples=docs.result_logs_destinations_samples,
    custom_api_filter_constructor=custom_api_filter_constructor,
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