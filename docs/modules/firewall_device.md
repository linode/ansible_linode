# firewall_device

Manage Linode Firewall Devices.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

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
| `firewall_id` | `int` | **Required** | The ID of the Firewall that contains this device.   |
| `entity_id` | `int` | **Required** | The ID for this Firewall Device. This will be the ID of the Linode Entity.   |
| `entity_type` | `str` | **Required** | The type of Linode Entity. Currently only supports linode.  (Choices:  `linode` ) |
| `state` | `str` | **Required** | The desired state of the target.  (Choices:  `present`  `absent` ) |






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
    - See the [Linode API response documentation](https://www.linode.com/docs/api/networking/#firewall-device-view__responses) for a list of returned fields


