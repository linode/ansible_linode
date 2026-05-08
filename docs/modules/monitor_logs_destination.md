# monitor_logs_destination

Manage logs destination that sevres as a sync point for logs data. You need read_write access to the scope to call this operation.

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
        endpoint_url: 'https://my-site.com/log-storage/database-info'
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
| [`details` (sub-options)](#details) | <center>`dict`</center> | <center>Optional</center> | Settings for the destination. For type 'akamai_object_storage': provide access_key_id, access_key_secret, bucket_name, host, and optionally path. For type 'custom_https_object': (fields to be added later).  **(Updatable)** |
| `label` | <center>`str`</center> | <center>Optional</center> | The name of the destination object. Used for display purposes.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of destination for log data sync, either akamai_object_storage if Object Storage is the destination, or custom_https for a unique URL  **(Choices: `akamai_object_storage`, `custom_https`; Updatable)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The unique identifier assigned to the logs destination. Run the List logs destinations operation and store the id for the applicable logs destination. Required for updating.   |
| `wait` | <center>`bool`</center> | <center>Optional</center> | Wait for the logs destination ready.  **(Default: `False`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | The amount of time, in seconds, to wait for the logs destination.  **(Default: `600`)** |

### details

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `basic_authentication_password` | <center>`str`</center> | <center>Optional</center> | The password tied to the basic_authentication_user, for basic authentication.  **(Updatable)** |
| `basic_authentication_user` | <center>`str`</center> | <center>Optional</center> | The user name for basic authentication.  **(Updatable)** |

### authentication

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| [`details` (sub-options)](#details) | <center>`dict`</center> | <center>Optional</center> | Includes additional parameters necessary to define basic authentication.If type is set to none, leave this object empty or out of a request.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of authentication in use. This can be None for no authentication, or basic for authentication using a username and password, set using the details parameters.  **(Choices: `none`, `basic`; Updatable)** |

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


