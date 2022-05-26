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
| `id` | `int` | Optional | The unique domain name of the Domain. Optional if `domain` is defined.   |
| `domain` | `str` | Optional | The unique id of the Domain. Optional if `id` is defined.   |





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


