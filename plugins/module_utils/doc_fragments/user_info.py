"""Documentation fragments for the user_info module"""

specdoc_examples = ['''
- name: Get info about a user
  linode.cloud.user_info:
    username: my-cool-user''']

result_user_samples = ['''{
  "email": "example_user@linode.com",
  "restricted": true,
  "user_type": "default",
  "ssh_keys": [
    "home-pc",
    "laptop"
  ],
  "tfa_enabled": null,
  "username": "example_user"
}''']

result_grants_samples = ['''{
  "domain": [
    {
      "id": 123,
      "label": "example-entity",
      "permissions": "read_only"
    }
  ],
  "global": {
    "account_access": "read_only",
    "add_databases": true,
    "add_domains": true,
    "add_firewalls": true,
    "add_images": true,
    "add_linodes": true,
    "add_longview": true,
    "add_nodebalancers": true,
    "add_stackscripts": true,
    "add_volumes": true,
    "cancel_account": false,
    "longview_subscription": true
  },
  "image": [
    {
      "id": 123,
      "label": "example-entity",
      "permissions": "read_only"
    }
  ],
  "linode": [
    {
      "id": 123,
      "label": "example-entity",
      "permissions": "read_only"
    }
  ],
  "longview": [
    {
      "id": 123,
      "label": "example-entity",
      "permissions": "read_only"
    }
  ],
  "nodebalancer": [
    {
      "id": 123,
      "label": "example-entity",
      "permissions": "read_only"
    }
  ],
  "stackscript": [
    {
      "id": 123,
      "label": "example-entity",
      "permissions": "read_only"
    }
  ],
  "volume": [
    {
      "id": 123,
      "label": "example-entity",
      "permissions": "read_only"
    }
  ]
}''']
