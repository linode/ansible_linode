"""Documentation fragments for the consumer_image_share_group_image_list module"""

specdoc_examples = ['''
- name: List all of the Image Share Group Images for the specified Token UUID
  linode.cloud.consumer_image_share_group_image_list: 
    token_uuid: "9e64b99e-92f7-4c7b-a616-8f622fffb94c"''']

result_consumer_image_share_group_images_samples = ['''[
    {
      "capabilities": [
        "cloud-init",
        "distributed-sites"
      ],
      "created": "2025-08-04T10:07:59",
      "created_by": null,
      "deprecated": true,
      "description": "Official Debian Linux image for server deployment",
      "eol": "2025-12-31T18:13:44.756Z",
      "expiry": "2025-12-31T18:13:44.756Z",
      "id": "shared/1",
      "image_sharing": {
        "shared_by": {
          "sharegroup_id": 123,
          "sharegroup_label": "DevOps Base Images",
          "sharegroup_uuid": "8d64b99e-92f7-4c7b-a616-8f622fffb94c",
          "source_image_id": "private/15"
        },
        "shared_with": null
      },
      "is_public": true,
      "is_shared": "none",
      "label": "Linux Debian",
      "regions": [
        {
          "region": "us-iad",
          "status": "available"
        }
      ],
      "size": 256,
      "status": "available",
      "tags": [
        "repair-image",
        "fix-1"
      ],
      "total_size": 256,
      "type": "shared",
      "updated": null,
      "vendor": "string"
    }
]''']
