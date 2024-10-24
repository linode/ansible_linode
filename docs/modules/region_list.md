# region_list

List and filter on Regions.

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
- name: List all of the Linode regions
  linode.cloud.region_list: {}
```

```yaml
- name: Filtered Linode regions
  linode.cloud.region_list:
    filters:
      - name: site_type
        values: core
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Regions in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Regions by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Regions.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Regions to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-regions).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `regions` - The returned Regions.

    - Sample Response:
        ```json
        [
            {
              "capabilities": [
                "Linodes",
                "Backups",
                "NodeBalancers",
                "Block Storage",
                "Object Storage",
                "Kubernetes",
                "Cloud Firewall",
                "Vlans",
                "VPCs",
                "Metadata",
                "Premium Plans"
              ],
              "country": "us",
              "id": "us-mia",
              "label": "Miami, FL",
              "resolvers": {
                "ipv4": "172.233.160.34, 172.233.160.27",
                "ipv6": "2a01:7e04::f03c:93ff:fead:d31f, 2a01:7e04::f03c:93ff:fead:d37f"
              },
              "site_type": "core",
              "status": "ok"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-regions) for a list of returned fields


