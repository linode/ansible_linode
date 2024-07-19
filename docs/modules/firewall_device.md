# firewall_device

Manage Linode Firewall Devices.

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
- name: Create a Firewall
  linode.cloud.firewall:
    label: my-firewall
    rules:
      inbound_policy: DROP
    state: present
  register: firewall_result

- name: Create an Instance
  linode.cloud.instance:
    label: my-instance
    region: us-east
    private_ip: true
    type: g6-standard-1
    state: present
  register: instance_result

- name: Attach the instance to the Firewall
  linode.cloud.firewall_device:
    firewall_id: '{{ firewall_result.firewall.id }}'
    entity_id: '{{ instance_result.instance.id }}'
    entity_type: 'linode'
    state: present
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `firewall_id` | <center>`int`</center> | <center>**Required**</center> | The ID of the Firewall that contains this device.   |
| `entity_id` | <center>`int`</center> | <center>**Required**</center> | The ID for this Firewall Device. This will be the ID of the Linode Entity.   |
| `entity_type` | <center>`str`</center> | <center>**Required**</center> | The type of Linode Entity. Currently only supports linode and nodebalancer.  **(Choices: `linode`, `nodebalancer`)** |
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |

## Return Values

- `device` - The Firewall Device in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2018-01-01T00:01:01",
          "entity": {
            "id": 123,
            "label": "my-linode",
            "type": "linode",
            "url": "/v4/linode/instances/123"
          },
          "id": 123,
          "updated": "2018-01-02T00:01:01"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-firewall-device) for a list of returned fields


