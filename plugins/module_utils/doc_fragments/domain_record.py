"""Documentation fragments for the domain_record module"""

specdoc_examples = ['''
- name: Create an A record
  linode.cloud.domain_record:
    domain: my-domain.com
    name: my-subdomain
    type: 'A'
    target: '127.0.0.1'
    state: present''', '''
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
    state: present''', '''
- name: Delete a domain record
  linode.cloud.domain_record:
    domain: my-domain.com
    name: my-subdomain
    type: 'A'
    target: '127.0.0.1'
    state: absent''', '''
- name: Delete the record by record_id
  linode.cloud.domain_record:            
    domain: my-domain.com
    record_id: 5678
    state: absent''']

result_record_samples = ['''{
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
}''']
