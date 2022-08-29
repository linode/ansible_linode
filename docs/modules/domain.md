# domain

Manage Linode Domains.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a domain 
  linode.cloud.domain:
    domain: my-domain.com
    type: master
    state: present
```

```yaml
- name: Delete a domain
  linode.cloud.domain:
    domain: my-domain.com
    state: absent
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `domain` | `str` | **Required** | The domain this Domain represents.   |
| `state` | `str` | **Required** | The desired state of the target.  (Choices:  `present` `absent`) |
| `axfr_ips` | `list` | Optional | The list of IPs that may perform a zone transfer for this Domain.   |
| `description` | `str` | Optional | The list of IPs that may perform a zone transfer for this Domain.   |
| `expire_sec` | `int` | Optional | The amount of time in seconds that may pass before this Domain is no longer authoritative.   |
| `master_ips` | `list` | Optional | The IP addresses representing the master DNS for this Domain.   |
| `refresh_sec` | `int` | Optional | The amount of time in seconds before this Domain should be refreshed.   |
| `retry_sec` | `int` | Optional | The interval, in seconds, at which a failed refresh should be retried.   |
| `soa_email` | `str` | Optional | The Start of Authority email address.   |
| `status` | `str` | Optional | Used to control whether this Domain is currently being rendered.   |
| `tags` | `list` | Optional | An array of tags applied to this object.   |
| `ttl_sec` | `int` | Optional | the amount of time in seconds that this Domain’s records may be cached by resolvers or other domain servers.   |
| `type` | `str` | Optional | Whether this Domain represents the authoritative source of information for the domain it describes (master), or whether it is a read-only copy of a master (slave).   |






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


