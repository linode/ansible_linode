# lke_version_list

List Kubernetes versions available for deployment to a Kubernetes cluster.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: List all Kubernetes versions available for deployment to a Kubernetes cluster
  linode.cloud.lke_versions: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list lke versions in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order lke versions by.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of results to return. If undefined, all results will be returned.   |

## Return Values

- `lke_versions` - The returned lke versions.

    - Sample Response:
        ```json
        [
            {
              "id": "1.25"
            }
        ]
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/linode-kubernetes-engine-lke/#kubernetes-versions-list__response-samples) for a list of returned fields


