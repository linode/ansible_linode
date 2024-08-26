"""Documentation fragments for the stackscript_list module"""

specdoc_examples = ['''
- name: List all of the stackscripts for the current Linode Account
  linode.cloud.stackscript_list: {}''', '''
- name: List the latest 5 stackscripts for the current Linode Account
  linode.cloud.stackscript_list:
    count: 5
    order_by: created
    order: desc''', '''
- name: List all personal stackscripts for the current Linode Account
  linode.cloud.stackscript_list:
    filters:
      - name: mine
        values: true''']

result_stackscripts_samples = ['''[
    {
        "created": "2018-01-01T00:01:01",
        "deployments_active": 1,
        "deployments_total": 12,
        "description": "This StackScript installs and configures MySQL\\n",
        "id": 10079,
        "images": [
            "linode/debian11",
            "linode/debian10"
        ],
        "is_public": true,
        "label": "a-stackscript",
        "mine": true,
        "rev_note": "Set up MySQL",
        "script": "\\\"#!/bin/bash\\\"\\n",
        "updated": "2018-01-01T00:01:01",
        "user_defined_fields": [
            {
                "default": null,
                "example": "hunter2",
                "label": "Enter the password",
                "manyOf": "avalue,anothervalue,thirdvalue",
                "name": "DB_PASSWORD",
                "oneOf": "avalue,anothervalue,thirdvalue"
            }
        ],
        "user_gravatar_id": "a445b305abda30ebc766bc7fda037c37",
        "username": "myuser"
    }
]''']
