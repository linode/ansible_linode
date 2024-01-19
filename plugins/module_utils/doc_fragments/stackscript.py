"""Documentation fragments for the volume module"""

specdoc_examples = ['''
- name: Create a basic StackScript
  linode.cloud.stackscript:
    label: my-stackscript
    images: ['linode/ubuntu22.04']
    description: Install a system package
    script: |
        #!/bin/bash
        # <UDF name="package" label="System Package to Install" example="nginx" default="">
        apt-get -q update && apt-get -q -y install $PACKAGE
    state: present''', '''
- name: Delete a StackScript
  linode.cloud.stackscript:
    label: my-stackscript
    state: absent''']

result_stackscript_samples = ['''{
  "created": "2018-01-01T00:01:01",
  "deployments_active": 1,
  "deployments_total": 12,
  "description": "This StackScript installs and configures MySQL",
  "id": 10079,
  "images": [
    "linode/debian11",
    "linode/debian10"
  ],
  "is_public": true,
  "label": "a-stackscript",
  "mine": true,
  "rev_note": "Set up MySQL",
  "script": "#!/bin/bash",
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
}''']
