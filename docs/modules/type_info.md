# type_info

Get info about a Linode Type.

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
- name: Get info about a Linode type by ID
  linode.cloud.type_info:
    id: g6-standard-2
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | The ID of the Type to resolve.   |

## Return Values

- `type` - The returned Type.

    - Sample Response:
        ```json
        
        {
            "addons": {
                "backups": {
                    "price": {
                        "hourly": 0.008,
                        "monthly": 5
                    }
                }
            },
            "class": "standard",
            "disk": 81920,
            "gpus": 0,
            "id": "g6-standard-2",
            "label": "Linode 4GB",
            "memory": 4096,
            "network_out": 1000,
            "price": {
                "hourly": 0.03,
                "monthly": 20
            },
            "successor": null,
            "transfer": 4000,
            "vcpus": 2
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-type) for a list of returned fields


