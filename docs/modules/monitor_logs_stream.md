# monitor_logs_stream

Create, update, and delete Monitor Logs Streams.

A stream defines a flow of logs (like audit logs) to a specific destination.

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
- name: Create a new monitor logs stream
  linode.cloud.monitor_logs_stream:
    label: "my-audit-logs"
    type: "audit_logs"
    status: "active"
    destinations:
      - 12345
    state: present
```

```yaml
- name: Update an existing stream's destinations
  linode.cloud.monitor_logs_stream:
    id: 9876
    label: "my-audit-logs-updated"
    destinations:
      - 54321
    state: present
```

```yaml
- name: Delete a monitor logs stream
  linode.cloud.monitor_logs_stream:
    id: 9876
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The desired state of the logs stream.  **(Choices: `present`, `absent`)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the logs stream. Used to identify an existing stream to update or delete.   |
| `label` | <center>`str`</center> | <center>Optional</center> | The name of the stream. This is used for display purposes in Akamai Cloud Manager.  **(Updatable)** |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of stream. This can be ``audit_logs`` for logs consisting of all of the control plane operations for the services in your Linodes, or ``lke_audit_logs`` for log data for your Linode Kubernetes Engine (LKE) enterprise clusters.  **(Choices: `audit_logs`, `lke_audit_logs`)** |
| [`details` (sub-options)](#details) | <center>`dict`</center> | <center>Optional</center> | Additional details for the stream, based on the selected type. Currently, this only applies to streams with a type of ``lke_audit_logs``.  **(Updatable)** |
| `status` | <center>`str`</center> | <center>Optional</center> | The availability status of the stream. While creating or updating, you can pass ``active`` or ``inactive``. Note that the API might return ``provisioning`` while it is being set up.  **(Choices: `active`, `inactive`; Updatable)** |
| `destinations` | <center>`list`</center> | <center>Optional</center> | List of unique identifiers for the sync points that will receive logs data. At the moment only a single destination is supported by the API.  **(Updatable)** |
| `wait` | <center>`bool`</center> | <center>Optional</center> | Wait for the stream to finish provisioning before returning.  **(Default: `False`)** |
| `wait_timeout` | <center>`int`</center> | <center>Optional</center> | Time in seconds to wait for the stream to finish provisioning.  **(Default: `600`)** |

### details

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `cluster_ids` | <center>`list`</center> | <center>Optional</center> | The unique identifiers for each LKE enterprise cluster.   |
| `is_auto_add_all_clusters_enabled` | <center>`bool`</center> | <center>Optional</center> | When set to ``true``, newly added LKE enterprise clusters on your account will be included in the stream. If ``false``, only existing LKE enterprise clusters are included.  **(Default: `False`)** |

## Return Values

- `stream` - A dictionary containing the details of the monitor logs stream.

    - Sample Response:
        ```json
        {
                "created": "2025-03-20 01:41:09",
                "created_by": "John Q. Linode",
                "destinations": [
                    {
                        "details": {
                            "access_key_id": "123",
                            "bucket_name": "primary-bucket",
                            "host": "primary-bucket-1.us-iad-12.linodeobjects.com",
                            "path": "audit-logs"
                        },
                        "id": 12345,
                        "label": "OBJ_logs_destination",
                        "type": "akamai_object_storage"
                    }
                ],
                "id": 12345,
                "label": "AuditLog-config",
                "status": "active",
                "type": "audit_logs",
                "updated": "2025-03-20 01:41:09",
                "updated_by": "Jane Q. Linode",
                "version": 1
            }
        ```


