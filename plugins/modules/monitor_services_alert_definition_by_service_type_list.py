#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list ACLP Monitor Service Alert Definitions
for a specific service type.
NOTE: This module is under v4beta."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    alert_definitions_by_service_type_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import (
    FieldType,
)

module = ListModule(
    result_display_name="Alert Definitions",
    result_field_name="alert_definitions",
    description=[
        "The return alert definitions by service type. "
        "**Note: filters and order are currently NOT supported by this endpoint."
    ],
    endpoint_template="/monitor/services/{service_type}/alert-definitions",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference"
    "/get-alert-definitions-for-service-type",
    examples=docs.specdoc_examples,
    result_samples=docs.result_alert_definitions_by_service_type_samples,
    requires_beta=True,
    params=[
        ListModuleParam(
            display_name="Service Type",
            name="service_type",
            type=FieldType.string,
        )
    ],
    # filtering is currently not supported by this module
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
