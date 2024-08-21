# domain

Manage Linode Domains.

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
| `domain` | <center>`str`</center> | <center>**Required**</center> | The domain this Domain represents.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| `axfr_ips` | <center>`list`</center> | <center>Optional</center> | The list of IPs that may perform a zone transfer for this Domain.  **(Updatable)** |
| `description` | <center>`str`</center> | <center>Optional</center> | The list of IPs that may perform a zone transfer for this Domain.  **(Updatable)** |
| `expire_sec` | <center>`int`</center> | <center>Optional</center> | The amount of time in seconds that may pass before this Domain is no longer authoritative.  **(Updatable)** |
| `master_ips` | <center>`list`</center> | <center>Optional</center> | The IP addresses representing the master DNS for this Domain.  **(Updatable)** |
| `refresh_sec` | <center>`int`</center> | <center>Optional</center> | The amount of time in seconds before this Domain should be refreshed.  **(Updatable)** |
| `retry_sec` | <center>`int`</center> | <center>Optional</center> | The interval, in seconds, at which a failed refresh should be retried.  **(Updatable)** |
| `soa_email` | <center>`str`</center> | <center>Optional</center> | The Start of Authority email address.  **(Updatable)** |
| `status` | <center>`str`</center> | <center>Optional</center> | Used to control whether this Domain is currently being rendered.  **(Updatable)** |
| `tags` | <center>`list`</center> | <center>Optional</center> | An array of tags applied to this object.  **(Updatable)** |
| `ttl_sec` | <center>`int`</center> | <center>Optional</center> | The amount of time in seconds that this Domain’s records may be cached by resolvers or other domain servers.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | Whether this Domain represents the authoritative source of information for the domain it describes (master), or whether it is a read-only copy of a master (slave).  **(Updatable)** |

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-domain) for a list of returned fields


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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-domain-record) for a list of returned fields


- `zone_file` - The zone file for the last rendered zone for the specified domain.

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


