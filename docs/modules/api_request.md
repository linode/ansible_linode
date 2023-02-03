# api_request

Make an arbitrary Linode API request.

The Linode API documentation can be found here: https://www.linode.com/docs/api


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Get all available LKE versions
  linode.cloud.api_request:
    path: lke/versions
    method: GET
```

```yaml
- name: Manually create a domain
  linode.cloud.api_request:
    path: domains
    method: POST
    body:
      domain: my-domain.com
      type: master
      soa_email: myemail@example.com
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `path` | <center>`str`</center> | <center>**Required**</center> | The relative path to the endpoint to make a request to. e.g. "linode/instances"   |
| `method` | <center>`str`</center> | <center>**Required**</center> | The HTTP method of the request or response.  **(Choices: `POST`, `PUT`, `GET`, `DELETE`)** |
| `body` | <center>`dict`</center> | <center>Optional</center> | The body of the request. This is a YAML structure that will be marshalled to JSON.  **(Conflicts With:`body_json`)** |
| `body_json` | <center>`str`</center> | <center>Optional</center> | The body of the request in JSON format.  **(Conflicts With:`body`)** |
| `filters` | <center>`dict`</center> | <center>Optional</center> | A YAML structure corresponding to the X-Filter request header. See: https://www.linode.com/docs/api/#filtering-and-sorting   |






## Return Values

- `body` - The deserialized response body.

    - Sample Response:
        ```json
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
        ```


- `status` - The response status code.


