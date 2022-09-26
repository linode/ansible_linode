# mysql

Manage a Linode Image.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a basic image from an existing disk
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    state: present
```

```yaml
- name: Create a basic image from a file
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    source_file: myimage.img.gz
    state: present
```

```yaml
- name: Delete an image
  linode.cloud.image:
    label: my-image
    state: absent
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | `str` | **Required** | This database's unique label.   |
| `state` | `str` | **Required** | The state of this database.  (Choices:  `present`  `absent` ) |
| `allow_list` | `list` | Optional | A list of IP addresses that can access the Managed Database. Each item can be a single IP address or a range in CIDR format.   |
| `cluster_size` | `int` | Optional | The number of Linode Instance nodes deployed to the Managed Database.  (Choices:  `1`  `3` Default: `1`) |
| `encrypted` | `bool` | Optional | Whether the Managed Databases is encrypted.   |
| `engine` | `str` | Optional | The Managed Database engine in engine/version format.   |
| `region` | `str` | Optional | The Region ID for the Managed Database.   |
| `replication_type` | `str` | Optional | The replication method used for the Managed Database. Defaults to none for a single cluster and semi_synch for a high availability cluster. Must be none for a single node cluster. Must be asynch or semi_synch for a high availability cluster.  (Choices:  `none`  `asynch`  `semi_synch` Default: `none`) |
| `ssl_connection` | `bool` | Optional | Whether to require SSL credentials to establish a connection to the Managed Database.  (Default: `True`) |
| `wait` | `bool` | Optional | Wait for the database to have status `available` before returning.  (Default: `True`) |
| `wait_timeout` | `int` | Optional | The amount of time, in seconds, to wait for an image to have status `available`.  (Default: `3600`) |






## Return Values

- `image` - The Image in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2021-08-14T22:44:02",
          "created_by": "linode",
          "deprecated": false,
          "description": "Example Image description.",
          "eol": "2026-07-01T04:00:00",
          "expiry": null,
          "id": "linode/debian11",
          "is_public": true,
          "label": "Debian 11",
          "size": 2500,
          "status": null,
          "type": "manual",
          "updated": "2021-08-14T22:44:02",
          "vendor": "Debian"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/images/#image-view__response-samples) for a list of returned fields


