# api_request

Make an arbitrary Linode API request.


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
| `path` | `str` | **Required** | The relative path to the endpoint to make a request to. e.g. "linode/instances"   |
| `method` | `str` | **Required** | The HTTP method of the request or response.  (Choices:  `POST`  `PUT`  `GET`  `DELETE` ) |
| `body` | `dict` | Optional | The body of the request. This is a YAML structure that will be marshalled to JSON.   |
| `body_json` | `str` | Optional | The body of the request in JSON format.   |
| `filters` | `dict` | Optional | A YAML structure corresponding to the X-Filter request header. See: https://www.linode.com/docs/api/#filtering-and-sorting   |






## Return Values

- `body` - The deserialized response body.

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


- `status` - The response status code.

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


