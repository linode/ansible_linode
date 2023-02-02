# domain_record_info

Get info about a Linode Domain Record.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `domain_id` | <center>`int`</center> | <center>Optional</center> | The ID of the parent Domain. Optional if `domain` is defined.   |
| `domain` | <center>`str`</center> | <center>Optional</center> | The name of the parent Domain. Optional if `domain_id` is defined.   |
| `id` | <center>`int`</center> | <center>Optional</center> | The unique id of the subdomain. Optional if `name` is defined.   |
| `name` | <center>`str`</center> | <center>Optional</center> | The name of the domain record. Optional if `id` is defined.   |






## Return Values

- `record` - View a single Record on this Domain.

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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/domains/#domain-record-view) for a list of returned fields


