# domain_record_info

Get info about a Linode Domain Records.

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
- name: Get info about domain records by name
  linode.cloud.domain_record_info:
    domain: my-domain.com
    name: my-subdomain
    type: A
    target: 0.0.0.0
```

```yaml
- name: Get info about a domain record by id
  linode.cloud.domain_info:
    domain: my-domain.com
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `domain_id` | <center>`int`</center> | <center>Optional</center> | The ID of the Domain ID for this resource.  **(Conflicts With: `domain`)** |
| `domain` | <center>`str`</center> | <center>Optional</center> | The ID of the Domain for this resource.  **(Conflicts With: `domain_id`)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Domain Records to resolve.  **(Conflicts With: `name`)** |
| `name` | <center>`str`</center> | <center>Optional</center> | The name of the Domain Records to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `record` - The returned Domain Records.

    - Sample Response:
        ```json
        {
          "created": "2018-01-01T00:01:01",
          "id": 123456,
          "name": "test",
          "port": 80,
          "priority": 50,
          "protocol": null,
          "service": null,
          "tag": null,
          "target": "192.0.2.0",
          "ttl_sec": 604800,
          "type": "A",
          "updated": "2018-01-01T00:01:01",
          "weight": 50
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-domain-record) for a list of returned fields


