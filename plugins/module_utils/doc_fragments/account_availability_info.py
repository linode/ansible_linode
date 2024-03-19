"""Documentation fragments for the account_availability module"""

result_account_availability_samples = ['''
{
  "region": "us-east",
  "unavailable": ["Linode"]
}
''']


specdoc_examples = ['''
- name: Get info about the current Linode account availability
  linode.cloud.account_info: 
    api_version: v4beta
    region: us-east
''']
