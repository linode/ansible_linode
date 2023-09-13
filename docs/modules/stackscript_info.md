# stackscript_info

Get info about a Linode StackScript.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about a StackScript by label
  linode.cloud.stackscript_info:
    label: my-stackscript
```

```yaml
- name: Get info about a StackScript by ID
  linode.cloud.stackscript_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the StackScript to resolve.   |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the StackScript to resolve.   |

## Return Values

- `stackscript` - The returned StackScript.

    - Sample Response:
        ```json
        {
          "created": "2018-01-01T00:01:01",
          "deployments_active": 1,
          "deployments_total": 12,
          "description": "This StackScript installs and configures MySQL",
          "id": 10079,
          "images": [
            "linode/debian9",
            "linode/debian8"
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


