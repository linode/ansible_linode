# monitor_logs_destination

Manage logs destination that serves as a sync point for logs data. You need read_write access to the scope to call this operation.

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
- name: Create logs destination with akamai object storage type
  linode.cloud.monitor_logs_destination:
    label: 'test-logs-destination'
    type: 'akamai_object_storage'
    details:
      access_key_id: '{{ access_key_id }}'
      access_key_secret: '{{ access_key_secret }}'
      bucket_name: '{{ bucket_name }}'
      host: '{{ host }}'
      path: 'test-path'
    state: present
```

```yaml
- name: Create logs destination with custom https endpoint type
  linode.cloud.monitor_logs_destination:
    label: 'test-logs-destination'
    type: 'custom_https'
    details:
      authentication:
        type: 'basic'
        details:
          basic_authentication_user: '{{ basic_authentication_user }}'
          basic_authentication_password: '{{ basic_authentication_password }}'
      client_certificate_details: 
        client_certificate: '{{ client_certificate }}'
        client_ca_certificate: '{{ client_ca_certificate }}'
        client_private_key: '{{ client_private_key }}'
        tls_hostname: 'my-site.com'
      content_type: 'application/json'
      custom_headers:
        - name: 'Cache-Control'
          value: 'max-age=0'
      data_compression: 'gzip'
      endpoint_url: 'https://my-site.com/log-storage/basicAuth'
    state: present
```

```yaml
- name: Update logs destination
  linode.cloud.monitor_logs_destination:
    id: 12345
    label: 'test-logs-updated'
    state: present
```

```yaml
- name: Delete logs destination
  linode.cloud.monitor_logs_destination:
    id: 12345
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the target.  **(Choices: `present`, `absent`)** |
| [`details` (sub-options)](#details) | <center>`dict`</center> | <center>Optional</center> | Settings for the destination. For type 'akamai_object_storage': provide access_key_id, access_key_secret, bucket_name, host and optionally path. For type 'custom_https': provide authentication, client_certificate_details, content_type, data_compression, endpoint_url and optionally custom_headers.  **(Updatable)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The name of the destination object. Used for display purposes.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of destination for log data sync, either akamai_object_storage if Object Storage is the destination, or custom_https for a unique URL  **(Choices: `akamai_object_storage`, `custom_https`; Updatable)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The unique identifier assigned to the logs destination. Run the List logs destinations operation and store the id for the applicable logs destination. Required for updating.   |
| `wait` | <center>`bool`</center> | <center>Optional</center> | Wait for the logs destination ready.  **(Default: `False`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The amount of time, in seconds, to wait for the logs destination.  **(Default: `600`)** |

### details

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `access_key_id` | <center>`str`</center> | <center>Optional</center> | The unique identifier assigned to the Object Storage key required for authentication to the bucket. Run the List Object Storage keys operation and store the id for the applicable key. (Required for type: akamai_object_storage)  **(Updatable)** |
| `access_key_secret` | <center>`str`</center> | <center>Optional</center> | The Object Storage key's secret key. This is used as a password to validate the key. (Required for type: akamai_object_storage)  **(Updatable)** |
| `bucket_name` | <center>`str`</center> | <center>Optional</center> | The name of the Object Storage bucket. Run the List Object Storage buckets operation and store the label for the target bucket. (Required for type: akamai_object_storage)  **(Updatable)** |
| `host` | <center>`str`</center> | <center>Optional</center> | The hostname where the Object Storage bucket can be accessed. Run the List Object Storage buckets operation and store the hostname for the target bucket. (Required for type: akamai_object_storage)  **(Updatable)** |
| `path` | <center>`str`</center> | <center>Optional</center> | Include this object to set a custom path for audit log storage in your Object Storage bucket. (Optional for type: akamai_object_storage)  **(Updatable)** |
| [`authentication` (sub-options)](#authentication) | <center>`dict`</center> | <center>Optional</center> | Authentication details required to access the endpoint_url. (Used for type: custom_https)  **(Updatable)** |
| [`client_certificate_details` (sub-options)](#client_certificate_details) | <center>`dict`</center> | <center>Optional</center> | Contains transport layer security (TLS) client certificate information to additionally secure the connection for the request. (Used for type: custom_https)  **(Updatable)** |
| `content_type` | <center>`str`</center> | <center>Optional</center> | The content type for requests to the endpoint_url. This can be application/json for request bodies formatted as JSON, or application/json; charset=utf-8 for JSON-format content encoded using UTF-8.(Used for type: custom_https)  **(Choices: `application/json`, `application/json; charset=utf-8`; Updatable)** |
| [`custom_headers` (sub-options)](#custom_headers) | <center>`list`</center> | <center>Optional</center> | Pairs of parameters used to optionally include custom headers in the request.(Used for type: custom_https)  **(Updatable)** |
| `data_compression` | <center>`str`</center> | <center>Optional</center> | Specifies whether data compression is applied to files included in a request. This can be gzip to apply this compression format or None.(Used for type: custom_https)  **(Choices: `gzip`, `None`; Updatable)** |
| `endpoint_url` | <center>`str`</center> | <center>Optional</center> | The URL where the request will be sent. (Used for type: custom_https)  **(Updatable)** |

### authentication

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`authentication_details` (sub-options)](#authentication_details) | <center>`dict`</center> | <center>Optional</center> | Includes additional parameters necessary to define basic authentication.If type is set to none, leave this object empty or out of a request.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of authentication in use. This can be None for no authentication, or basic for authentication using a username and password, set using the details parameters.  **(Choices: `none`, `basic`; Updatable)** |

### authentication_details

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `basic_authentication_password` | <center>`str`</center> | <center>Optional</center> | The password tied to the basic_authentication_user, for basic authentication.  **(Updatable)** |
| `basic_authentication_user` | <center>`str`</center> | <center>Optional</center> | The user name for basic authentication.  **(Updatable)** |

### client_certificate_details

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `client_ca_certificate` | <center>`str`</center> | <center>Optional</center> | The certificate authority (CA) certificate used to verify a requesting server's identity.  **(Updatable)** |
| `client_certificate` | <center>`str`</center> | <center>Optional</center> | The PEM-formatted digital certificate you want to authenticate requests to your destination with.  **(Updatable)** |
| `client_private_key` | <center>`str`</center> | <center>Optional</center> | The private key in the non-encrypted PKCS8 format that authenticates with the back-end server. If you want to use mutual authentication, you need to provide both the client_certificate and the client_private_key.  **(Updatable)** |
| `tls_hostname` | <center>`str`</center> | <center>Optional</center> | The hostname that verifies the server's certificate and matches the Subject Alternative Names (SANs) in the certificate. If not provided, the API fetches the hostname from the endpoint_url.  **(Updatable)** |

### custom_headers

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>**Required**</center> | The name of the custom header to include in the request.  **(Updatable)** |
| `value` | <center>`str`</center> | <center>**Required**</center> | The body content for the custom header to include in the request.  **(Updatable)** |

## Return Values

- `logs_destination` - The logs destination in JSON serialized form.

    - Sample Response:
        ```json
        {
          "created": "2025-07-20 09:45:13",
          "created_by": "John Q. Linode",
          "details": {
            "access_key_id": 123,
            "bucket_name": "primary-bucket",
            "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
            "path": "audit-logs"
          },
          "id": 12345,
          "label": "OBJ_logs_destination",
          "status": "active",
          "type": "akamai_object_storage",
          "updated": "2025-07-21 12:41:09",
          "updated_by": "Jane Q. Linode",
          "version": 1
        }
        ```
        ```json
        {
          "created": "2025-07-20T09:45:13",
          "created_by": "John Q. Linode",
          "details": {
            "authentication": {
              "details": {
                "basic_authentication_password": "p@$$w0Rd",
                "basic_authentication_user": "John_Q"
              },
              "type": "basic"
            },
            "client_certificate_details": {},
            "content_type": "application/json",
            "custom_headers": [
              {
                "name": "Cache-Control",
                "value": "max-age=0"
              }
            ],
            "data_compression": "gzip",
            "endpoint_url": "https://my-site.com/log-storage/database-info"
          },
          "id": 12346,
          "label": "custom_logs_destination",
          "type": "custom_https",
          "updated": "2025-07-21T12:41:09",
          "updated_by": "Jane Q. Linode"
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-destination) for a list of returned fields


