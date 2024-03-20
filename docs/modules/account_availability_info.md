# account_availability_info

Get info about a Linode Account Availability.

**:warning: This module makes use of beta endpoints and requires the `api_version` field be explicitly set to `v4beta`.**

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get info about the current Linode account availability
  linode.cloud.account_info: 
    api_version: v4beta
    region: us-east

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `region` | <center>`str`</center> | <center>**Required**</center> | The Region of the Account Availability to resolve.   |
| `api_token` | <center>`str`</center> | <center>Optional</center> | The Linode account personal access token. It is necessary to run the module. It can be exposed by the environment variable `LINODE_API_TOKEN` instead.   |

## Return Values

- `account_availability` - The returned Account Availability.

    - Sample Response:
        ```json
        
        {
          "region": "us-east",
          "unavailable": ["Linode"]
        }
        
        ```
    - See the [Linode API response documentation](TBD) for a list of returned fields


