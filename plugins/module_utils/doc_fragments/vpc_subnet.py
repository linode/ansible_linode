"""Documentation fragments for the vpc module"""

specdoc_examples = ['''
- name: Create a VPC Subnet
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    ipv4: '10.0.0.0/24'
    state: present''', '''
- name: Delete a VPC Subnet
  linode.cloud.vpc_subnet:
    vpc_id: 12345
    label: my-subnet
    state: absent''']

result_subnet_samples = ['''{
    "created": "2023-08-31T18:53:04",
    "id": 271,
    "ipv4": "10.0.0.0/24",
    "label": "test-subnet",
    "linodes": [
        {
            "id": 1234567,
            "interfaces": [{"active": false, "id": 654321}]
        }
    ],
    "updated": "2023-08-31T18:53:04"
}''']
