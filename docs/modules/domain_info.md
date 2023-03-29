# domain_info

Get info about a Linode Domain.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `id` | <center>`int`</center> | <center>Optional</center> | The unique domain name of the Domain. Optional if `domain` is defined.  **(Conflicts With: `domain`)** |
| `domain` | <center>`str`</center> | <center>Optional</center> | The unique id of the Domain. Optional if `id` is defined.  **(Conflicts With: `id`)** |

## Return Values

- `domain` - The domain in JSON serialized form.

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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/domains/#domain-view) for a list of returned fields


- `records` - The domain record in JSON serialized form.

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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/domains/#domain-record-view) for a list of returned fields


- `zone_file` - The zone file for the last rendered zone for the specified domain.

    - Sample Response:
        ```json
        [
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
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/domains/#domain-zone-file-view) for a list of returned fields


