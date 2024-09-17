# child_account_list

List and filter on Child Account.

NOTE: Parent/Child related features may not be generally available.

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
- name: List all of the Child Accounts under the current Account
  linode.cloud.child_account_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Child Account in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Child Account by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Child Account.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Child Account to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-child-accounts).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `child_accounts` - The returned Child Account.

    - Sample Response:
        ```json
        {
            "active_since": "2018-01-01T00:01:01",
            "address_1": "123 Main Street",
            "address_2": "Suite A",
            "balance": 200,
            "balance_uninvoiced": 145,
            "billing_source": "external",
            "capabilities": [
                "Linodes",
                "NodeBalancers",
                "Block Storage",
                "Object Storage"
            ],
            "city": "Philadelphia",
            "company": "Linode LLC",
            "country": "US",
            "credit_card": {
                "expiry": "11/2022",
                "last_four": 1111
            },
            "email": "john.smith@linode.com",
            "euuid": "E1AF5EEC-526F-487D-B317EBEB34C87D71",
            "first_name": "John",
            "last_name": "Smith",
            "phone": "215-555-1212",
            "state": "PA",
            "tax_id": "ATU99999999",
            "zip": "19102-1234"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-child-accounts) for a list of returned fields


