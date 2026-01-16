# image_share_group_image_list

List and filter on Image Share Group Images.

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
- name: List all of the Image Share Group Images for the specified Share Group
  linode.cloud.image_share_group_image_list: 
    sharegroup_id: 123
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `sharegroup_id` | <center>`int`</center> | <center>**Required**</center> | The parent Image Share Group for the Image Share Group Images.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Image Share Group Images in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Image Share Group Images by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Image Share Group Images.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Image Share Group Images to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-images).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `image_share_group_images` - The returned Image Share Group Images.

    - Sample Response:
        ```json
        [
            {
              "capabilities": [
                "cloud-init",
                "distributed-sites"
              ],
              "created": "2025-08-04T10:07:59",
              "created_by": null,
              "deprecated": true,
              "description": "Official Debian Linux image for server deployment",
              "eol": "2025-12-31T18:13:44.756Z",
              "expiry": "2025-12-31T18:13:44.756Z",
              "id": "shared/1",
              "image_sharing": {
                "shared_by": {
                  "sharegroup_id": 123,
                  "sharegroup_label": "DevOps Base Images",
                  "sharegroup_uuid": "8d64b99e-92f7-4c7b-a616-8f622fffb94c",
                  "source_image_id": "private/15"
                },
                "shared_with": null
              },
              "is_public": true,
              "is_shared": "none",
              "label": "Linux Debian",
              "regions": [
                {
                  "region": "us-iad",
                  "status": "available"
                }
              ],
              "size": 256,
              "status": "available",
              "tags": [
                "repair-image",
                "fix-1"
              ],
              "total_size": 256,
              "type": "shared",
              "updated": null,
              "vendor": "string"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-sharegroup-images) for a list of returned fields


