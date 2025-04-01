# lke_version_list

List and filter on LKE Versions.

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
    - name: List all Kubernetes versions available for deployment to a Kubernetes cluster
      linode.cloud.lke_version_list:
    
```

```yaml
    - name: List all enterprise-tier Kubernetes versions available for deployment to a Kubernetes cluster
      linode.cloud.lke_version_list:
        tier: "enterprise"
    
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list LKE Versions in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order LKE Versions by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting LKE Versions.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of LKE Versions to return. If undefined, all results will be returned.   |
| `tier` | <center>`str`</center> | <center>Optional</center> | Specifies the service tier for retrieving LKE version details. NOTE: LKE Enterprise may not currently be available to all users  and can only be used with v4beta.  **(Choices: `standard`, `enterprise`)** |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-lke-versions).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `lke_versions` - The returned LKE Versions.

    - Sample Response:
        ```json
        
            [
                {
                    "id": "1.32"
                },
                {
                    "id": "1.31"
                },
                {
                    "id": "1.30"
                }
            ]
            
        ```
        ```json
        
            [
                {
                    "id": "v1.31.1+lke1",
                    "tier": "enterprise"
                }
            ]
            
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lke-versions) for a list of returned fields


