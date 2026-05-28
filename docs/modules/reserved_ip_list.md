# reserved_ip_list

List and filter on Reserved IPs.

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
- name: List all reserved IPs for the current Linode Account
  linode.cloud.reserved_ip_list: {}
```

```yaml
- name: List reserved IPs filtered by tag
  linode.cloud.reserved_ip_list:
    filters:
      - name: tags
        values:
          - lb
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Reserved IPs in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Reserved IPs by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Reserved IPs.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Reserved IPs to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-reserved-ips).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `reserved_ips` - The returned Reserved IPs.

    - Sample Response:
        ```json
        [
          {
            "address": "192.0.2.141",
            "assigned_entity": null,
            "gateway": "192.0.2.1",
            "interface_id": null,
            "linode_id": null,
            "prefix": 24,
            "public": true,
            "rdns": "",
            "region": "us-east",
            "reserved": true,
            "subnet_mask": "255.255.255.0",
            "tags": [
              "lb",
              "prod"
            ],
            "type": "ipv4",
            "vpc_nat_1_1": null
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-reserved-ips) for a list of returned fields


