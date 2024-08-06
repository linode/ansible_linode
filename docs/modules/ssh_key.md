# ssh_key

Manage a Linode SSH key.

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
- name: Create a basic SSH key
  linode.cloud.ssh_key:
    label: my-ssh-key
    state: present
```

```yaml
- name: Delete a SSH key
  linode.cloud.ssh_key:
    label: my-ssh-key
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `label` | <center>`str`</center> | <center>**Required**</center> | This SSH key's unique label.   |
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of this SSH key.  **(Choices: `present`, `absent`)** |
| `ssh_key` | <center>`str`</center> | <center>Optional</center> | The SSH public key value.   |

## Return Values

- `ssh_key` - The created SSH key in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2018-01-01T00:01:01",
          "id": 42,
          "label": "My SSH Key",
          "ssh_key": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/post-add-ssh-key) for a list of returned fields


