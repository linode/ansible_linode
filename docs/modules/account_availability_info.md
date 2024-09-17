# account_availability_info

Get info about a Linode Account Availability.

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
- name: Get info about the current Linode account availability
  linode.cloud.account_availability_info: 
    api_version: v4beta
    region: us-east

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `region` | <center>`str`</center> | <center>**Required**</center> | The Region of the Account Availability to resolve.   |

## Return Values

- `account_availability` - The returned Account Availability.

    - Sample Response:
        ```json
        
        {
          "region": "us-east",
          "available": ["NodeBalancers", "Block Storage", "Kubernetes"],
          "unavailable": ["Linode"]
        }
        
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-account-availability) for a list of returned fields


