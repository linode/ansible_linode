"""Documentation fragments for the api_request module"""

specdoc_examples = ['''
- name: Get all available LKE versions
  linode.cloud.api_request:
    path: lke/versions
    method: GET''', '''
- name: Manually create a domain
  linode.cloud.api_request:
    path: domains
    method: POST
    body:
      domain: my-domain.com
      type: master
      soa_email: myemail@example.com''']

result_body_samples = ['''{
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
}''']
