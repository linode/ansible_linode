# reserved_ip

Manage a Linode Reserved IPv4 Address.

NOTE: Reserved IP feature may not currently be available to all users.

NOTE: When creating a reservation by region (without specifying an address), 

this module is NOT idempotent — each run will allocate a new billable reserved 

IP address. To manage an existing reservation idempotently, 

specify the address parameter.

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
# WARNING: This task is NOT idempotent. Re-running it will allocate
# a new billable reserved IP each time. Specify 'address' to manage
# an existing reservation idempotently.
- name: Reserve an IP in us-east
  linode.cloud.reserved_ip:
    region: us-east
    state: present
  register: reserved_ip
```

```yaml
- name: Reserve an IP with tags
  linode.cloud.reserved_ip:
    region: us-east
    tags:
      - lb
      - prod
    state: present
```

```yaml
- name: Unreserve (delete) a reserved IP
  linode.cloud.reserved_ip:
    address: "192.0.2.141"
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this reserved IP address.  **(Choices: `present`, `absent`)** |
| `region` | <center>`str`</center> | <center>Optional</center> | The Region in which to reserve the IP address. Required when creating a new reservation (state=present without an existing address).   |
| `address` | <center>`str`</center> | <center>Optional</center> | The reserved IPv4 address. Required when deleting (state=absent) or updating an existing reserved IP.   |
| `tags` | <center>`list`</center> | <center>Optional</center> | Tags to apply to this reserved IP address. NOTE: Tags are replaced entirely on update, not appended.  **(Updatable)** |

## Return Values

- `reserved_ip` - The reserved IP address in JSON serialized form.

    - Sample Response:
        ```json
        {
          "address": "192.0.2.141",
          "assigned_entity": null,
          "gateway": "192.0.2.1",
          "interface_id": null,
          "linode_id": null,
          "prefix": 24,
          "public": true,
          "rdns": "",
          "region": "us-east",
          "reserved": true,
          "subnet_mask": "255.255.255.0",
          "tags": [
            "lb",
            "prod"
          ],
          "type": "ipv4",
          "vpc_nat_1_1": null
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-reserved-ip) for a list of returned fields


