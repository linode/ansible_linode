#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list entities associated with a specific
ACLP Monitor Service Alert Definition.
NOTE: This module is under v4beta."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    alert_definition_entities_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="Alert Definition Entities",
    result_field_name="alert_definition_entities",
    endpoint_template="/monitor/services/{service_type}/alert-definitions/{id}/entities",
    result_docs_url="TODO",
    examples=docs.specdoc_examples,
    result_samples=docs.result_alert_definition_entities_samples,
    requires_beta=True,
    params=[
        ListModuleParam(
            display_name="Service Type",
            name="service_type",
            type=FieldType.string,
        ),
        ListModuleParam(
            display_name="Alert Definition",
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
