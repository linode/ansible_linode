# domain_record

Manage Linode Domain Records.

NOTE: Domain records are identified by their name, target, and type.

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
- name: Create an A record
  linode.cloud.domain_record:
    domain: my-domain.com
    name: my-subdomain
    type: 'A'
    target: '127.0.0.1'
    state: present
```

```yaml
- name: Create an SRV domain record
  linode.cloud.domain_record:
    domain: my-domain.com
    service: srv-service
    protocol: tcp
    type: 'SRV'
    target: host.example.com
    port: 443
    priority: 0
    weight: 1
    state: present
```

```yaml
- name: Delete a domain record
  linode.cloud.domain_record:
    domain: my-domain.com
    name: my-subdomain
    type: 'A'
    target: '127.0.0.1'
    state: absent
```

```yaml
- name: Delete the record by record_id
  linode.cloud.domain_record:            
    domain: my-domain.com
    record_id: 5678
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `domain_id` | <center>`int`</center> | <center>Optional</center> | The ID of the parent Domain.   |
| `domain` | <center>`str`</center> | <center>Optional</center> | The name of the parent Domain.   |
| `record_id` | <center>`int`</center> | <center>Optional</center> | The id of the record to modify.  **(Conflicts With: `name`)** |
| `name` | <center>`str`</center> | <center>Optional</center> | The name of this Record. NOTE: If the name of the record ends with the domain, it will be dropped from the resulting record's name. Unused for SRV record. Use the service property to set the service name for this record.  **(Conflicts With: `record_id`)** |
| `port` | <center>`int`</center> | <center>Optional</center> | The port this Record points to. Only valid and required for SRV record requests.  **(Updatable)** |
| `priority` | <center>`int`</center> | <center>Optional</center> | The priority of the target host for this Record. Lower values are preferred. Only valid for MX and SRV record requests. Required for SRV record requests.  **(Updatable)** |
| `protocol` | <center>`str`</center> | <center>Optional</center> | The protocol this Record’s service communicates with. An underscore (_) is prepended automatically to the submitted value for this property.  **(Updatable)** |
| `service` | <center>`str`</center> | <center>Optional</center> | An underscore (_) is prepended and a period (.) is appended automatically to the submitted value for this property. Only valid and required for SRV record requests. The name of the service.  **(Updatable)** |
| `tag` | <center>`str`</center> | <center>Optional</center> | The tag portion of a CAA record. Only valid and required for CAA record requests.  **(Updatable)** |
| `target` | <center>`str`</center> | <center>Optional</center> | The target for this Record.   |
| `ttl_sec` | <center>`int`</center> | <center>Optional</center> | The amount of time in seconds that this Domain’s records may be cached by resolvers or other domain servers.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of Record this is in the DNS system.   |
| `weight` | <center>`int`</center> | <center>Optional</center> | The relative weight of this Record used in the case of identical priority.  **(Updatable)** |

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-domain-record) for a list of returned fields


