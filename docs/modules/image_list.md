# image_list

List and filter on Images.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://www.linode.com/docs/api/images/#images-list__responses).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `images` - The returned Images.

    - Sample Response:
        ```json
        [
           {
              "created":"2021-08-14T22:44:02",
              "created_by":"linode",
              "deprecated":false,
              "description":"Example Image description.",
              "eol":"2026-07-01T04:00:00",
              "expiry":null,
              "id":"linode/debian11",
              "is_public":true,
              "label":"Debian 11",
              "size":2500,
              "status":null,
              "type":"manual",
              "updated":"2021-08-14T22:44:02",
              "vendor":"Debian"
           }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/images/#images-list__responses) for a list of returned fields


