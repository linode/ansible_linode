# maintenance_policy_list

List and filter on Maintenance Policies.

WARNING! This module makes use of beta endpoints and requires the C(api_version) field be explicitly set to C(v4beta).

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
- name: List all of the Linode Maintenance Policies
  linode.cloud.maintenance_policy_list: {}
```

```yaml

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Maintenance Policies in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Maintenance Policies by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Maintenance Policies.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Maintenance Policies to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-maintenance-policies).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `maintenance_policies` - The returned Maintenance Policies.

    - Sample Response:
        ```json
        [
            {
              "slug": "linode/migrate",
              "label": "Migrate",
              "description": "Migrates the Linode to a new host while it remains fully operational. Recommended for maximizing availability.",
              "type": "migrate",
              "notification_period_sec": 300,
              "is_default": true
            },
            {
              "slug": "linode/power_off_on",
              "label": "Power-off/on",
              "description": "Powers off the Linode at the start of the maintenance event and reboots it once the maintenance finishes. Recommended for maximizing performance.",
              "type": "power_off_on",
              "notification_period_sec": 1800,
              "is_default": false
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-maintenance-policies) for a list of returned fields


