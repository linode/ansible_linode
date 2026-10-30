"""Documentation fragments for the lock_list module"""

specdoc_examples = [
    """
- name: List all locks for the current account
  linode.cloud.lock_list: {}""",
    """
- name: List all locks with a specific lock type
  linode.cloud.lock_list:
    filters:
      - name: lock_type
        values: cannot_delete""",
    """
- name: List all locks for a specific entity type
  linode.cloud.lock_list:
    filters:
      - name: entity.type
        values: linode""",
]

result_locks_samples = [
  """[
  {
    "id": 1,
    "lock_type": "cannot_delete_with_subresources",
    "entity": {
      "id": 290349,
      "type": "linode",
      "label": "linode290349",
      "url": "/v4/linode/instances/290349"
    }
  }
]"""
]
