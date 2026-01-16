# image_share_group_list

List and filter on Image Share Groups.

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
- name: List all of the Image Share Groups for the current Linode Account
  linode.cloud.image_share_group_list: {}
```

```yaml
- name: List all of the Image Share Groups that contain a specific private image
  linode.cloud.image_share_group_list:
    image_id: "private/12345"
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Image Share Groups in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Image Share Groups by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Image Share Groups.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Image Share Groups to return. If undefined, all results will be returned.   |
| `image_id` | <center>`str`</center> | <center>Optional</center> | Specifies the private image ID to list share groups for. If provided, only share groups containing the specified image will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-sharegroups).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `image_share_groups` - The returned Image Share Groups.

    - Sample Response:
        ```json
        [
            {
              "created": "2025-04-14T22:44:02",
              "description": "Group of base operating system images and engineers used for CI/CD pipelines and infrastructure automation",
              "expiry": null,
              "id": 1,
              "images_count": 0,
              "is_suspended": false,
              "label": "DevOps Base Images",
              "members_count": 0,
              "updated": null,
              "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroups) for a list of returned fields


