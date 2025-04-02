# lke_version_info

Get info about a Linode LKE Version.

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
    - name: Get info about an LKE version by ID
      linode.cloud.lke_cluster_info:
        id: '1.31'
    
```

```yaml
    - name: Get info about an LKE version by tier and ID
      linode.cloud.lke_cluster_info:
        tier: 'standard'
        id: '1.31'
    
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | The ID of the LKE Version to resolve.   |
| `tier` | <center>`str`</center> | <center>Optional</center> | Specifies the service tier for retrieving LKE version details. NOTE: LKE Enterprise may not currently be available to all users and  can only be used with v4beta.  **(Choices: `standard`, `enterprise`)** |

## Return Values

- `lke_version` - The returned LKE Version.

    - Sample Response:
        ```json
        
            {
              "id": "1.31"
            }
            
        ```
        ```json
        
            {
              "id": "1.31",
              "tier": "standard"
            }
            
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-version) for a list of returned fields


