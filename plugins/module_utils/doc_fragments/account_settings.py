"""Documentation fragments for the account settings module"""

specdoc_examples = ['''
- name: Retrieve
  linode.cloud.account_settings:
    state: present''']

result_account_settings_samples = ['''{
  "backups_enabled": true,
  "interfaces_for_new_linodes": "linode_only",
  "longview_subscription": "longview-3",
  "managed": true,
  "network_helper": false,
  "object_storage": "active",
  "maintenance_policy": "linode/migrate"
}''']
