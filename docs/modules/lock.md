# lock

Create and delete Linode resource locks.

Resource locks protect resources from accidental deletion.

Locks can only be created and deleted by unrestricted users.

NOTE: Locks cannot be updated. To change a lock, delete it and create a new one.

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
- name: Create a lock on a Linode instance
  linode.cloud.lock:
    entity_type: linode
    entity_id: 12345
    lock_type: cannot_delete
    state: present
```

```yaml
- name: Create a lock with subresource protection
  linode.cloud.lock:
    entity_type: linode
    entity_id: 12345
    lock_type: cannot_delete_with_subresources
    state: present
```

```yaml
- name: Create a lock on a NodeBalancer
  linode.cloud.lock:
    entity_type: nodebalancer
    entity_id: 12345
    lock_type: cannot_delete
    state: present
```

```yaml
- name: Delete a lock by ID
  linode.cloud.lock:
    id: 67890
    state: absent
```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `state` | <center>`str`</center> | <center>**Required**</center> | The state of the lock.  **(Choices: `present`, `absent`)** |
| `id` | <center>`int`</center> | <center>Optional</center> | The ID of the lock to delete. Only used when state is absent; ignored when state is present.   |
| `entity_type` | <center>`str`</center> | <center>Optional</center> | The type of entity to lock. Supported entity types: 'linode', 'volume', 'nodebalancer', 'lkecluster', 'lkenodepool'.  **(Choices: `linode`, `volume`, `nodebalancer`, `lkecluster`, `lkenodepool`)** |
| `entity_id` | <center>`int`</center> | <center>Optional</center> | The ID of the entity to lock.   |
| `lock_type` | <center>`str`</center> | <center>Optional</center> | The type of lock to apply. Only one delete-protection lock may exist per resource at a time. 'cannot_delete' - Prevents deletion of the entity. 'cannot_delete_with_subresources' - Prevents deletion of the  entity and its subresources (disks, configs, etc.).  **(Choices: `cannot_delete`, `cannot_delete_with_subresources`)** |

## Return Values

- `lock` - The lock in JSON serialized form.

    - Sample Response:
        ```json
        {
            "id": 1,
            "lock_type": "cannot_delete",
            "entity": {
                "id": 6003234,
                "type": "linode",
                "label": "my-linode",
                "url": "/v4/linode/instances/6003234"
            }
        }
        ```
    - See the [Linode API response documentation](https://techdocs.akamai.com/linode-api/reference/get-lock) for a list of returned fields


