# region_info

Get info about a Linode Region.

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
- name: Get Info of a Linode Region
  linode.cloud.region_info:
    id: us-mia
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | The ID of the Region to resolve.   |

## Return Values

- `region` - The returned Region.

    - Sample Response:
        ```json
        {
            "id": "us-mia",
            "label": "Miami, FL",
            "country": "us",
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
                "Premium Plans",
                "Placement Group"
            ],
            "status": "ok",
            "resolvers": {
                "ipv4": "172.233.160.34, 172.233.160.27, 172.233.160.30, 172.233.160.29, 172.233.160.32, 172.233.160.28, 172.233.160.33, 172.233.160.26, 172.233.160.25, 172.233.160.31",
                "ipv6": "2a01:7e04::f03c:93ff:fead:d31f, 2a01:7e04::f03c:93ff:fead:d37f, 2a01:7e04::f03c:93ff:fead:d30c, 2a01:7e04::f03c:93ff:fead:d318, 2a01:7e04::f03c:93ff:fead:d316, 2a01:7e04::f03c:93ff:fead:d339, 2a01:7e04::f03c:93ff:fead:d367, 2a01:7e04::f03c:93ff:fead:d395, 2a01:7e04::f03c:93ff:fead:d3d0, 2a01:7e04::f03c:93ff:fead:d38e"
            },
            "placement_group_limits": {
                "maximum_pgs_per_customer": null,
                "maximum_linodes_per_pg": 5
            },
            "site_type": "core"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-region) for a list of returned fields


