"""Documentation fragments for the image_info module"""

specdoc_examples = ['''
- name: List all of the images for the current Linode Account
  linode.cloud.image_list: {}''', '''
- name: List the latest 5 images for the current Linode Account
  linode.cloud.image_list:
    count: 5
    order_by: created
    order: desc''', '''
- name: Resolve all Alpine Linux images
  linode.cloud.image_list:
    filters:
      - name: vendor
        values: Alpine''']

result_images_samples = ['''[
    {
      "capabilities": [
        "cloud-init",
        "distributed-sites"
      ],
      "created": "2021-08-14T22:44:02",
      "created_by": "linode",
      "deprecated": false,
      "description": "Example image description.",
      "eol": "2026-07-01T04:00:00",
      "expiry": null,
      "id": "private/15",
      "image_sharing": {
        "shared_by": null,
        "shared_with": {
          "sharegroup_count": 0,
          "sharegroup_list_url": "/images/private/15/sharegroups"
        }
      },
      "is_public": false,
      "is_shared": false,
      "label": "Debian 11",
      "regions": [
        {
          "region": "us-iad",
          "status": "available"
        }
      ],
      "size": 2500,
      "status": "available",
      "tags": [
        "repair-image",
        "fix-1"
      ],
      "total_size": 1234567,
      "type": "manual",
      "updated": "2021-08-14T22:44:02",
      "vendor": "Debian"
    }
]''']
