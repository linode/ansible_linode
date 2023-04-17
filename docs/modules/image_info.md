# image_info

Get info about a Linode Image.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `id` | <center>`str`</center> | <center>Optional</center> | The ID of the image.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the image.  **(Conflicts With: `id`)** |

## Return Values

- `image` - The image in JSON serialized form.

    - Sample Response:
        ```json
        {
          "capabilities": [],
          "created": "2021-08-14T22:44:02",
          "created_by": "linode",
          "deprecated": false,
          "description": "Example Image description.",
          "eol": "2026-07-01T04:00:00",
          "expiry": null,
          "id": "linode/debian11",
          "is_public": true,
          "label": "Debian 11",
          "size": 2500,
          "status": null,
          "type": "manual",
          "updated": "2021-08-14T22:44:02",
          "vendor": "Debian"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/images/#image-view__responses) for a list of returned fields


