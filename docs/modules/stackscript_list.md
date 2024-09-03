# stackscript_list

List and filter on StackScripts.

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
- name: List all of the stackscripts for the current Linode Account
  linode.cloud.stackscript_list: {}
```

```yaml
- name: List the latest 5 stackscripts for the current Linode Account
  linode.cloud.stackscript_list:
    count: 5
    order_by: created
    order: desc
```

```yaml
- name: List all personal stackscripts for the current Linode Account
  linode.cloud.stackscript_list:
    filters:
      - name: mine
        values: true
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list StackScripts in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order StackScripts by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting StackScripts.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of StackScripts to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-stack-scripts).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `stackscripts` - The returned StackScripts.

    - Sample Response:
        ```json
        [
            {
                "created": "2018-01-01T00:01:01",
                "deployments_active": 1,
                "deployments_total": 12,
                "description": "This StackScript installs and configures MySQL\n",
                "id": 10079,
                "images": [
                    "linode/debian11",
                    "linode/debian10"
                ],
                "is_public": true,
                "label": "a-stackscript",
                "mine": true,
                "rev_note": "Set up MySQL",
                "script": "\"#!/bin/bash\"\n",
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-stack-scripts) for a list of returned fields


