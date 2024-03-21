# domain_list

List and filter on Domains.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all of the domains for the current Linode Account
  linode.cloud.domain_list: {}
```

```yaml
- name: Resolve all domains for the current Linode Account
  linode.cloud.domain_list:
    filters:
      - name: domain
        values: example.org
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `api_token` | <center>`str`</center> | <center>Optional</center> | The Linode account personal access token. It is necessary to run the module. It can be exposed by the environment variable `LINODE_API_TOKEN` instead.   |
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list domains in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order domains by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting domains.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable attributes can be found here: https://www.linode.com/docs/api/domains/#domains-list__responses#domains-list__responses   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `domains` - The returned domains.

    - Sample Response:
        ```json
        [
            {
              "axfr_ips": [],
              "description": null,
              "domain": "example.org",
              "expire_sec": 300,
              "group": null,
              "id": 1234,
              "master_ips": [],
              "refresh_sec": 300,
              "retry_sec": 300,
              "soa_email": "admin@example.org",
              "status": "active",
              "tags": [
                "example tag",
                "another example"
              ],
              "ttl_sec": 300,
              "type": "master"
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/domains/#domains-list__response-samples) for a list of returned fields


