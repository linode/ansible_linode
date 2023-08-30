#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode VPCs."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModuleBase,
)


class ListModule(ListModuleBase):
    display_name = "VPC"
    result_field = "vpcs"
    endpoint = "/vpcs"
    docs_url = "TODO"


SPECDOC_META = ListModule.spec

if __name__ == "__main__":
    ListModule()
