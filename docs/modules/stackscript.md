# stackscript

Manage a Linode StackScript.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a basic StackScript
  linode.cloud.stackscript:
    label: my-stackscript
    images: ['linode/ubuntu20.04']
    description: Install a system package
    script: |
        #!/bin/bash
        # <UDF name="package" label="System Package to Install" example="nginx" default="">
        apt-get -q update && apt-get -q -y install $PACKAGE
    state: present
```

```yaml
- name: Delete a StackScript
  linode.cloud.stackscript:
    label: my-stackscript
    state: absent
```









## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | `str` | **Required** | This StackScript's unique label.   |
| `state` | `str` | **Required** | The state of this StackScript.  (Choices:  `present` `absent`) |
| `description` | `str` | Optional | A description for the StackScript.   |
| `images` | `list` | Optional | Images that can be deployed using this StackScript.   |
| `is_public` | `bool` | Optional | This determines whether other users can use your StackScript.   |
| `rev_note` | `str` | Optional | This field allows you to add notes for the set of revisions made to this StackScript.   |
| `script` | `str` | Optional | The script to execute when provisioning a new Linode with this StackScript.   |





## Return Values

- `stackscript` - The StackScript in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2018-01-01T00:01:01",
          "deployments_active": 1,
          "deployments_total": 12,
          "description": "This StackScript installs and configures MySQL
        ",
          "id": 10079,
          "images": [
            "linode/debian9",
            "linode/debian8"
          ],
          "is_public": true,
          "label": "a-stackscript",
          "mine": true,
          "rev_note": "Set up MySQL",
          "script": ""#!/bin/bash"
        ",
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
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/stackscripts/#stackscript-create__response-samples) for a list of returned fields


