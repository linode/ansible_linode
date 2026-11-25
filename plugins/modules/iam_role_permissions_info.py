#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to view IAM role permissions."""

from typing import Any, Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    iam_role_permissions as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    iam_role_permissions_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType, SpecField
from linode_api4 import LinodeClient


def _get_role_permissions(
    client: LinodeClient, params: Dict[str, Any]
) -> Dict[str, Any]:
    username = params.get("username")

    if username:
        return client.iam.role_permissions_user_get(username)

    return client.iam.role_permissions()


module = InfoModule(
    description=[
        "View IAM role permissions.",
        "If `username` is specified, the roles assigned to that user are returned; "
        "otherwise the roles and permissions available on the account are returned.",
    ],
    primary_result=InfoModuleResult(
        display_name="IAM Role Permissions",
        field_name="role_permissions",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-user-role-permissions",
        samples=docs_parent.result_role_permissions_samples
        + docs.result_available_samples,
        get=_get_role_permissions,
    ),
    custom_options={
        "username": SpecField(
            type=FieldType.string,
            description=[
                "The username of the user to view assigned roles for.",
                "If not specified, the roles available on the account are returned.",
            ],
        )
    },
    requires_beta=True,
    examples=docs.specdoc_examples,
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
