# domain_record_info

Get info about a Linode Domain Records.


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



- `domain_id` (`int`) -  The ID of the parent Domain.  
- `domain` (`str`) -  The name of the parent Domain.  
- `id` (`int`) -  The unique id of the subdomain.  
- `name` (`str`) -  The name of the domain record.  


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


