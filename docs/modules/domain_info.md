# domain_info

Get info about a Linode Domain.

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
- name: Get info about a domain by domain
  linode.cloud.domain_info:
    domain: my-domain.com
```

```yaml
- name: Get info about a domain by id
  linode.cloud.domain_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the Domain to resolve.  **(Conflicts With: `domain`)** |
| `domain` | <center>`str`</center> | <center>Optional</center> | The domain of the Domain to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `domain` - The returned Domain.

    - Sample Response:
        ```json
        {
          "axfr_ips": [],
          "description": null,
          "domain": "example.org",
          "expire_sec": 300,
          "group": null,
          "id": 1234,
          "master_ips": [],
          "refresh_sec": 300,
          "retry_sec": 300,
          "soa_email": "admin@example.org",
          "status": "active",
          "tags": [
            "example tag",
            "another example"
          ],
          "ttl_sec": 300,
          "type": "master"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-domain) for a list of returned fields


- `records` - The returned records.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-domain-records) for a list of returned fields


- `zone_file` - The returned zone file.

    - Sample Response:
        ```json
        {
          "zone_file": [
            "; example.com [123]",
            "$TTL 864000",
            "@  IN  SOA  ns1.linode.com. user.example.com. 2021000066 14400 14400 1209600 86400",
            "@    NS  ns1.linode.com.",
            "@    NS  ns2.linode.com.",
            "@    NS  ns3.linode.com.",
            "@    NS  ns4.linode.com.",
            "@    NS  ns5.linode.com."
          ]
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-domain-zone) for a list of returned fields


