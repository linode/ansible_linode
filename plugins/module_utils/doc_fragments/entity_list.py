"""Documentation fragments for the entity_list module"""

specdoc_examples = [
    """
- name: List all entities for the current account
  linode.cloud.entity_list: {}""",
]

result_entities_samples = [
    """[
  {
    "id": 123,
    "label": "my-linode",
    "type": "linode"
  }
]"""
]
