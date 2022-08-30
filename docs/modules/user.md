# user

Manage a Linode User.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a basic user
  linode.cloud.user:
    username: my-cool-user
    email: user@linode.com
    restricted: false
    state: present
```

```yaml
- name: Delete a user
  linode.cloud.user:
    username: my-cool-user
    state: absent
```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `username` | `str` | **Required** | The username of this user.   |
| `state` | `str` | **Required** | The state of this user.  (Choices:  `present` `absent`) |
| `restricted` | `bool` | Optional | If true, the User must be granted access to perform actions or access entities on this Account.  ( Default: `True`) |
| `email` | `str` | Optional | The email address for the User. Linode sends emails to this address for account management communications. May be used for other communications as configured.   |






## Return Values

- `user` - The user in JSON serialized form.

    - Sample Response:
        ```json
        {
          "email": "example_user@linode.com",
          "restricted": true,
          "ssh_keys": [
            "home-pc",
            "laptop"
          ],
          "tfa_enabled": null,
          "username": "example_user"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/account/#user-view__response-samples) for a list of returned fields


