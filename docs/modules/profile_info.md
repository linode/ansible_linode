# profile_info

Get info about a Linode Profile.

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
- name: Get info about the current Linode profile
  linode.cloud.profile_info: {}
```


## Return Values

- `profile` - The returned Profile.

    - Sample Response:
        ```json
        {
          "authentication_type": "password",
          "authorized_keys": [
            null
          ],
          "email": "example-user@gmail.com",
          "email_notifications": true,
          "ip_whitelist_enabled": false,
          "lish_auth_method": "keys_only",
          "referrals": {
            "code": "871be32f49c1411b14f29f618aaf0c14637fb8d3",
            "completed": 0,
            "credit": 0,
            "pending": 0,
            "total": 0,
            "url": "https://www.linode.com/?r=871be32f49c1411b14f29f618aaf0c14637fb8d3"
          },
          "restricted": false,
          "timezone": "US/Eastern",
          "two_factor_auth": true,
          "uid": 1234,
          "username": "exampleUser",
          "verified_phone_number": "+5555555555"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-profile) for a list of returned fields


