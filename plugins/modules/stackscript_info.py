#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode StackScript."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModuleAttr,
    InfoModuleBase,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import StackScript


class Module(InfoModuleBase):
    """Module for getting info about a Linode StackScript"""

    display_name = "StackScript"
    response_field = "stackscript"
    response_sample = {}

    attributes = {
        "id": InfoModuleAttr(
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                StackScript, params.get("id")
            )._raw_json,
        ),
        "label": InfoModuleAttr(
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: client.linode.stackscripts(
                StackScript.label == params.get("label")
            )[0]._raw_json,
        ),
    }


SPECDOC_META = Module.spec

if __name__ == "__main__":
    Module()
