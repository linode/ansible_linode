# domain_record

Manage Linode Domain Records.

NOTE: Domain records are identified by their name, target, and type.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create an A record
  linode.cloud.domain_record:
    domain: my-domain.com
    name: my-subdomain
    type: 'A'
    target: '127.0.0.1'
    state: present
```

```yaml
- name: Delete a domain record
  linode.cloud.domain:
    domain: my-domain.com
    name: my-subdomain
    state: absent
```









## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | `str` | **Required** | The desired state of the target.  (Choices:  `present` `absent`) |
| `domain_id` | `int` | Optional | The ID of the parent Domain.   |
| `domain` | `str` | Optional | The name of the parent Domain.   |
| `record_id` | `int` | Optional | The id of the record to modify.   |
| `name` | `str` | Optional | The name of this Record.   |
| `port` | `int` | Optional | The port this Record points to. Only valid and required for SRV record requests.   |
| `priority` | `int` | Optional | The priority of the target host for this Record. Lower values are preferred. Only valid for MX and SRV record requests. Required for SRV record requests.   |
| `protocol` | `str` | Optional | The protocol this Record’s service communicates with. An underscore (_) is prepended automatically to the submitted value for this property.   |
| `service` | `str` | Optional | An underscore (_) is prepended and a period (.) is appended automatically to the submitted value for this property. Only valid and required for SRV record requests. The name of the service.   |
| `tag` | `str` | Optional | The tag portion of a CAA record. Only valid and required for CAA record requests.   |
| `target` | `str` | Optional | The target for this Record.   |
| `ttl_sec` | `int` | Optional | The amount of time in seconds that this Domain’s records may be cached by resolvers or other domain servers.   |
| `type` | `str` | Optional | The type of Record this is in the DNS system.   |
| `weight` | `int` | Optional | The relative weight of this Record used in the case of identical priority.   |





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


