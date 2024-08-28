#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list SSH keys in their Linode profile."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ssh_key_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="SSH Keys",
    result_field_name="ssh_keys",
    endpoint_template="/profile/sshkeys",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-ssh-keys",
    examples=docs.ssh_key_list_specdoc_examples,
    result_samples=docs.result_ssh_key_list_samples,
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
