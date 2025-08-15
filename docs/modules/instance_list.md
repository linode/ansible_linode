# instance_list

List and filter on Instances.

- [Minimum Required Fields](#minimum-required-fields)
- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Minimum Required Fields
| Field       | Type  | Required     | Description                                                                                                                                                                                                              |
|-------------|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api_token` | `str` | **Required** | The Linode account personal access token. It is necessary to run the module. <br/>It can be exposed by the environment variable `LINODE_API_TOKEN` instead. <br/>See details in [Usage](https://github.com/linode/ansible_linode?tab=readme-ov-file#usage). |

## Examples

```yaml
- name: List all of the instances for the current Linode Account
  linode.cloud.instance_list: {}
```

```yaml
- name: Resolve all instances for the current Linode Account
  linode.cloud.instance_list:
    filters:
      - name: label
        values: myInstanceLabel
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Instances in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Instances by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Instances.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Instances to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-linode-instances).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `instances` - The returned Instances.

    - Sample Response:
        ```json
        [
           {
              "alerts": {
                "cpu": 180,
                "io": 10000,
                "network_in": 10,
                "network_out": 10,
                "transfer_quota": 80
              },
              "backups": {
                "available": true,
                "enabled": true,
                "last_successful": "2018-01-01T00:01:01",
                "schedule": {
                  "day": "Saturday",
                  "window": "W22"
                }
              },
              "created": "2018-01-01T00:01:01",
              "group": "Linode-Group",
              "host_uuid": "example-uuid",
              "hypervisor": "kvm",
              "id": 123,
              "image": "linode/debian11",
              "ipv4": [
                "203.0.113.1",
                "192.0.2.1"
              ],
              "ipv6": "c001:d00d::1337/128",
              "label": "linode123",
              "region": "us-east",
              "specs": {
                "disk": 81920,
                "memory": 4096,
                "transfer": 4000,
                "vcpus": 2
              },
              "status": "running",
              "tags": [
                "example tag",
                "another example"
              ],
              "type": "g6-standard-1",
              "updated": "2018-01-01T00:01:01",
              "watchdog_enabled": true,
              "disk_encryption": "enabled",
              "lke_cluster_id": null,
              "maintenance_policy": "linode/migrate"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-linode-instances) for a list of returned fields


