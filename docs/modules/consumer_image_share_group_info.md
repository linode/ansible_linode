# consumer_image_share_group_info

Get info about a Linode Image Share Group.

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
- name: Get info about an Image Share Group by a Consumer's Token UUID
  linode.cloud.consumer_image_share_group_info:
    token_uuid: "1433863e-16a4-47b5-b829-ac0f35c13278"
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `token_uuid` | <center>`str`</center> | <center>**Required**</center> | The ID of the Token for this resource.   |

## Return Values

- `image_share_group` - The returned Image Share Group.

    - Sample Response:
        ```json
        {
          "created": "2025-04-14T22:44:02",
          "description": "Group of base operating system images and engineers used for CI/CD pipelines and infrastructure automation",
          "id": 1,
          "is_suspended": false,
          "label": "DevOps Base Images",
          "updated": "2025-04-14T22:44:03",
          "uuid": "1533863e-16a4-47b5-b829-ac0f35c13278"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-by-token) for a list of returned fields


