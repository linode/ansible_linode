# image_list

List and filter on Images.

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
- name: List all of the images for the current Linode Account
  linode.cloud.image_list: {}
```

```yaml
- name: List the latest 5 images for the current Linode Account
  linode.cloud.image_list:
    count: 5
    order_by: created
    order: desc
```

```yaml
- name: Resolve all Alpine Linux images
  linode.cloud.image_list:
    filters:
      - name: vendor
        values: Alpine
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Images in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Images by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Images.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Images to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-images).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `images` - The returned Images.

    - Sample Response:
        ```json
        [
           {
              "created":"2021-08-14T22:44:02",
              "created_by":"my-account",
              "deprecated":false,
              "description":"Example Image description.",
              "eol":"2026-07-01T04:00:00",
              "expiry":null,
              "id":"private/123",
              "is_public":false,
              "label":"test",
              "size":2500,
              "status":null,
              "type":"manual",
              "updated":"2021-08-14T22:44:02",
              "vendor":"Debian",
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
                }]
               }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-images) for a list of returned fields


