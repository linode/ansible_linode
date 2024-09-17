# image_info

Get info about a Linode Image.

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
- name: Get info about an image by label
  linode.cloud.image_info:
    label: my-image
```

```yaml
- name: Get info about an image by ID
  linode.cloud.image_info:
    id: private/12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | The ID of the Image to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the Image to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `image` - The returned Image.

    - Sample Response:
        ```json
        {
          "capabilities": [],
          "created": "2021-08-14T22:44:02",
          "created_by": "my-account",
          "deprecated": false,
          "description": "Example Image description.",
          "eol": "2026-07-01T04:00:00",
          "expiry": null,
          "id": "private/123",
          "is_public": true,
          "label": "my-image",
          "size": 2500,
          "status": null,
          "type": "manual",
          "updated": "2021-08-14T22:44:02",
          "vendor": "Debian",
          "tags": ["test"],
          "total_size": 5000,
          "regions": [
            {
                "region": "us-east",
                "status": "available"
            },
            {
                "region": "us-central",
                "status": "pending"
            }
          ]
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-image) for a list of returned fields


