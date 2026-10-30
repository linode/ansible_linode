"""Documentation fragments for the lock module"""

specdoc_examples = [
    """
- name: Create a lock on a Linode instance
  linode.cloud.lock:
    entity_type: linode
    entity_id: 12345
    lock_type: cannot_delete
    state: present""",
    """
- name: Create a lock with subresource protection
  linode.cloud.lock:
    entity_type: linode
    entity_id: 12345
    lock_type: cannot_delete_with_subresources
    state: present""",
    """
- name: Create a lock on a NodeBalancer
  linode.cloud.lock:
    entity_type: nodebalancer
    entity_id: 12345
    lock_type: cannot_delete
    state: present""",
    """
- name: Delete a lock by ID
  linode.cloud.lock:
    id: 67890
    state: absent""",
]

result_lock_samples = [
    """{
    "id": 1,
    "lock_type": "cannot_delete",
    "entity": {
        "id": 6003234,
        "type": "linode",
        "label": "my-linode",
        "url": "/v4/linode/instances/6003234"
    }
}"""
]
