"""Documentation fragments for the iam_role_permissions_info module"""

specdoc_examples = [
    """
- name: List the roles and permissions available on the account
  linode.cloud.iam_role_permissions_info: {}""",
    """
- name: Get the roles assigned to a user
  linode.cloud.iam_role_permissions_info:
    username: my-user""",
]

result_available_samples = [
    """{
  "account_access": [
    {
      "type": "account",
      "roles": [
        {
          "name": "account_admin",
          "description": "Access to perform any supported action on all entities of the account",
          "permissions": ["create_linode", "update_linode"]
        }
      ]
    }
  ],
  "entity_access": [
    {
      "type": "linode",
      "roles": [
        {
          "name": "linode_contributor",
          "description": "Access to update a linode instance",
          "permissions": ["update_linode", "view_linode"]
        }
      ]
    }
  ]
}"""
]
