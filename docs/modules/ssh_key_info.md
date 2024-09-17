# ssh_key_info

Get info about a Linode SSH Key.

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
- name: Get info about a SSH key by label
  linode.cloud.ssh_key_info:
    label: my-ssh-key
```

```yaml
- name: Get info about a SSH key by ID
  linode.cloud.ssh_key_info:
    id: 12345
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the SSH Key to resolve.  **(Conflicts With: `label`)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The label of the SSH Key to resolve.  **(Conflicts With: `id`)** |

## Return Values

- `ssh_key` - The returned SSH Key.

    - Sample Response:
        ```json
        {
          "created": "2018-01-01T00:01:01",
          "id": 42,
          "label": "My SSH Key",
          "ssh_key": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-ssh-key) for a list of returned fields


