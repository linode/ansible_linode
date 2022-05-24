# firewall_device

Manage Linode Firewall Devices.


## Examples

```yaml["\n- name: Create a Firewall\n  linode.cloud.firewall:\n    label: my-firewall\n    rules:\n      inbound_policy: DROP\n    state: present\n  register: firewall_result\n\n- name: Create an Instance\n  linode.cloud.instance:\n    label: my-instance\n    region: us-east\n    private_ip: true\n    type: g6-standard-1\n    state: present\n  register: instance_result\n\n- name: Attach the instance to the Firewall\n  linode.cloud.firewall_device:\n    firewall_id: '{{ firewall_result.firewall.id }}'\n    entity_id: '{{ instance_result.instance.id }}'\n    entity_type: 'linode'\n    state: present"]
```


## Parameters


- `firewall_id` - **(Required)** The ID of the Firewall that contains this device. 
- `entity_id` - **(Required)** The ID for this Firewall Device. This will be the ID of the Linode Entity. 
- `entity_type` - **(Required)** The type of Linode Entity. Currently only supports linode. 


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


