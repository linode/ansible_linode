#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Node Balancer Types."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_type_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Node Balancer Types",
    result_field_name="nodebalancer_types",
    endpoint_template="/nodebalancers/types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_nodebalancer_type_samples,
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
