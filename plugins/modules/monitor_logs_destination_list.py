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
    Ensures 'id' values in filters are integers.
    """
    filters = params.get("filters")
    if filters:
        for f in filters:
            if f.get("name") == "id":
                # Convert all id values to int if possible
                f["values"] = [int(v) if isinstance(v, str) and v.isdigit() else v for v in f["values"]]
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
    result_field_name="destinations",
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