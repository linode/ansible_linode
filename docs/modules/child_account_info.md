# child_account_info

Get info about a Linode Child Account.

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
- name: Get info about a Child Account by EUUID
  linode.cloud.child_account_info:
    euuid: "FFFFFFFF-FFFF-FFFF-FFFFFFFFFFFFFFFF"
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `euuid` | <center>`str`</center> | <center>**Required**</center> | The EUUID of the Child Account to resolve.   |

## Return Values

- `child_account` - The returned Child Account.

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
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-child-account) for a list of returned fields


