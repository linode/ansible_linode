"""Documentation fragments for the linode.cloud.object_storage_endpoint_list module."""

specdoc_examples = ['''
- name: List all available Object Storage Endpoints
  linode.cloud.object_storage_endpoint_list: {}''']

result_endpoints_sample = ['''[
  {
    "endpoint_type": "E0",
    "region": "us-southeast",
    "s3_endpoint": "us-southeast-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E0",
    "region": "us-east",
    "s3_endpoint": "us-east-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "us-iad",
    "s3_endpoint": "us-iad-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "us-mia",
    "s3_endpoint": "us-mia-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "fr-par",
    "s3_endpoint": "fr-par-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E3",
    "region": "gb-lon",
    "s3_endpoint": "gb-lon-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E2",
    "region": "sg-sin-2",
    "s3_endpoint": "sg-sin-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "us-ord",
    "s3_endpoint": "us-ord-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "us-sea",
    "s3_endpoint": "us-sea-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E2",
    "region": "au-mel",
    "s3_endpoint": "au-mel-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "id-cgk",
    "s3_endpoint": "id-cgk-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "in-maa",
    "s3_endpoint": "in-maa-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "se-sto",
    "s3_endpoint": "se-sto-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "it-mil",
    "s3_endpoint": "it-mil-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "jp-osa",
    "s3_endpoint": "jp-osa-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "es-mad",
    "s3_endpoint": "es-mad-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "us-lax",
    "s3_endpoint": "us-lax-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "nl-ams",
    "s3_endpoint": "nl-ams-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E0",
    "region": "ap-south",
    "s3_endpoint": "ap-south-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E1",
    "region": "br-gru",
    "s3_endpoint": "br-gru-1.linodeobjects.com"
  },
  {
    "endpoint_type": "E0",
    "region": "eu-central",
    "s3_endpoint": "eu-central-1.linodeobjects.com"
  }
]''']
