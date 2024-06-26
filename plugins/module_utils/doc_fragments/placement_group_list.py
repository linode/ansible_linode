"""Documentation fragments for the placement_group_list module"""

specdoc_examples = ['''
- name: List all of Linode placement group for the current account
  linode.cloud.placement_group_list:
    api_version: v4beta''']

result_placement_groups_samples = ['''[
    {
      "id": 123,
      "label": "test",
      "region": "eu-west",
      "affinity_type": "anti_affinity:local",
      "is_strict": true,
      "is_compliant": true,
      "members": [
        {
          "linode_id": 123,
          "is_compliant": true
        }
      ]
    }
]''']
