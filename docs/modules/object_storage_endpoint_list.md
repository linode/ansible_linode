# object_storage_endpoint_list

List and filter on Object Storage Endpoints.

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
- name: List all available Object Storage Endpoints
  linode.cloud.object_storage_endpoint_list: {}
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `order` | <center>`str`</center> | <center>Optional</center> | The order to list Object Storage Endpoints in.  **(Choices: `desc`, `asc`; Default: `asc`)** |
| `order_by` | <center>`str`</center> | <center>Optional</center> | The attribute to order Object Storage Endpoints by.   |
| [`filters` (sub-options)](#filters) | <center>`list`</center> | <center>Optional</center> | A list of filters to apply to the resulting Object Storage Endpoints.   |
| `count` | <center>`int`</center> | <center>Optional</center> | The number of Object Storage Endpoints to return. If undefined, all results will be returned.   |

### filters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the field to filter on. Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-object-storage-endpoints).   |
| `values` | <center>`list`</center> | <center>**Required**</center> | A list of values to allow for this field. Fields will pass this filter if at least one of these values matches.   |

## Return Values

- `endpoints` - The returned Object Storage Endpoints.

    - Sample Response:
        ```json
        [
          {
            "endpoint_type": "E0",
            "region": "us-southeast",
            "s3_endpoint": "us-southeast-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E0",
            "region": "us-east",
            "s3_endpoint": "us-east-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "us-iad",
            "s3_endpoint": "us-iad-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "us-mia",
            "s3_endpoint": "us-mia-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "fr-par",
            "s3_endpoint": "fr-par-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E3",
            "region": "gb-lon",
            "s3_endpoint": "gb-lon-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E2",
            "region": "sg-sin-2",
            "s3_endpoint": "sg-sin-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "us-ord",
            "s3_endpoint": "us-ord-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "us-sea",
            "s3_endpoint": "us-sea-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E2",
            "region": "au-mel",
            "s3_endpoint": "au-mel-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "id-cgk",
            "s3_endpoint": "id-cgk-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "in-maa",
            "s3_endpoint": "in-maa-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "se-sto",
            "s3_endpoint": "se-sto-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "it-mil",
            "s3_endpoint": "it-mil-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "jp-osa",
            "s3_endpoint": "jp-osa-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "es-mad",
            "s3_endpoint": "es-mad-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "us-lax",
            "s3_endpoint": "us-lax-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "nl-ams",
            "s3_endpoint": "nl-ams-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E0",
            "region": "ap-south",
            "s3_endpoint": "ap-south-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E1",
            "region": "br-gru",
            "s3_endpoint": "br-gru-1.linodeobjects.com"
          },
          {
            "endpoint_type": "E0",
            "region": "eu-central",
            "s3_endpoint": "eu-central-1.linodeobjects.com"
          }
        ]
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-object-storage-endpoints) for a list of returned fields


