# stackscript

Manage a Linode StackScript.

- [Minimum Required Fields](#minimum-required-fields)
- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Minimum Required Fields
| Field       | Type  | Required     | Description                                                                                                                                                                                                              |
|-------------|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api_token` | `str` | **Required** | The Linode account personal access token. It is necessary to run the module. <br/>It can be exposed by the environment variable `LINODE_API_TOKEN` instead. <br/>See details in [Usage](https://github.com/linode/ansible_linode?tab=readme-ov-file#usage). |

## Examples

```yaml
- name: Create a basic StackScript
  linode.cloud.stackscript:
    label: my-stackscript
    images: ['linode/ubuntu22.04']
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
| `label` | <center>`str`</center> | <center>**Required**</center> | This StackScript's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this StackScript.  **(Choices: `present`, `absent`)** |
| `description` | <center>`str`</center> | <center>Optional</center> | A description for the StackScript.  **(Updatable)** |
| `images` | <center>`list`</center> | <center>Optional</center> | Images that can be deployed using this StackScript.  **(Updatable)** |
| `is_public` | <center>`bool`</center> | <center>Optional</center> | This determines whether other users can use your StackScript.  **(Updatable)** |
| `rev_note` | <center>`str`</center> | <center>Optional</center> | This field allows you to add notes for the set of revisions made to this StackScript.  **(Updatable)** |
| `script` | <center>`str`</center> | <center>Optional</center> | The script to execute when provisioning a new Linode with this StackScript.  **(Updatable)** |

## Return Values

- `stackscript` - The StackScript in JSON serialized form.

    - Sample Response:
        ```json
        {
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
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/post-add-stack-script) for a list of returned fields


