# vlans_list

List and filter on Linode VLANs.


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
    order_by: desc
    order: created
```

```yaml
- name: Resolve all Alpine Linux images
  linode.cloud.image_list:
    filter:
      - name: vendor
        values: Alpine
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | `str` | Optional | The order to list events in.  (Choices:  `desc`  `asc` Default: `asc`) |
| `order_by` | `str` | Optional | The attribute to order events by.   |
| [`filters` (sub-options)](#filters) | `list` | Optional | A list of filters to apply to the resulting events.   |
| `count` | `int` | Optional | The number of results to return. If undefined, all results will be returned.   |





### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | `str` | **Required** | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/images/#images-list__responses   |
| `values` | `list` | **Required** | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |






## Return Values

- `images` - The returned images.

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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/images/#images-list__response-samples) for a list of returned fields


