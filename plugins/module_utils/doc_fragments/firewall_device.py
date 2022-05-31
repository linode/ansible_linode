"""Documentation fragments for the firewall_device module"""

specdoc_examples = ['''
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
    state: present''']

result_device_samples = ['''{
  "created": "2018-01-01T00:01:01",
  "entity": {
    "id": 123,
    "label": "my-linode",
    "type": "linode",
    "url": "/v4/linode/instances/123"
  },
  "id": 123,
  "updated": "2018-01-02T00:01:01"
}''']
