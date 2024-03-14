"""Documentation fragments for the account_availability_list module"""

specdoc_examples = ['''
- name: List all of the region resource availabilities to the account
  linode.cloud.account_availability_list:
    api_version: v4beta''']

result_account_availabilities_samples = ['''[
    {
      "region": "ap-west",
      "unavailable": ["Linode"]
    },
    {
      "region": "ca-central",
      "unavailable": ["Linode", "Block Storage"]
    }
]''']
