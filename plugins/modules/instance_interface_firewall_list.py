#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Implementation for the linode.cloud.instance_interface_firewall_list module."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    instance_interface_firewall_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="Linode Interface Firewalls",
    result_field_name="firewalls",
    endpoint_template="/linode/interfaces/{linode_id}/interfaces/{interface_id}/firewalls",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/"
    + "get-linode-interface-firewalls",
    result_samples=docs.result_firewalls_samples,
    examples=docs.specdoc_examples,
    params=[
        ListModuleParam(
            display_name="Instance", name="linode_id", type=FieldType.integer
        ),
        ListModuleParam(
            display_name="Linode Interface",
            name="interface_id",
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
