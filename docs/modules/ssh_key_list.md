# ssh_key_list

List and filter on SSH Keys.

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
- name: List all of the SSH keys for the current Linode Account
  linode.cloud.ssh_key_list: {}
```

```yaml
- name: List the latest 5 SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:

    count: 5
    order_by: created
    order: desc
```

```yaml
- name: List filtered personal SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:

    filters:
      - name: label-or-some-other-field
        values: MySSHKey1
```

```yaml
- name: List filtered personal SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:
    filters:
      - name: label-or-some-other-field
        values:
          - MySSHKey1
          - MySSHKey2
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list SSH Keys in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order SSH Keys by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting SSH Keys.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of SSH Keys to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-ssh-keys).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `ssh_keys` - The returned SSH Keys.

    - Sample Response:
        ```json
        [
            {
              "created": "2018-01-01T00:01:01",
              "id": 42,
              "label": "MySSHKey1",
              "ssh_key": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
            }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-ssh-keys) for a list of returned fields


