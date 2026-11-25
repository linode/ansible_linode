"""Documentation fragments for the iam_role_permissions module"""

specdoc_examples = [
    """
- name: Assign roles to a user
  linode.cloud.iam_role_permissions:
    username: my-user
    account_access:
      - account_linode_admin
    entity_access:
      - id: 123
        type: linode
        roles:
          - linode_contributor""",
    """
- name: Remove all entity-level roles from a user
  linode.cloud.iam_role_permissions:
    username: my-user
    entity_access: []""",
]

result_role_permissions_samples = [
    """{
  "account_access": [
    "account_linode_admin"
  ],
  "entity_access": [
    {
      "id": 123,
      "type": "linode",
      "roles": [
        "linode_contributor"
      ]
    }
  ]
}"""
]
