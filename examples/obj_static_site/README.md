# Object Storage Static Site

| This example is intended to provide usage examples for the Linode Ansible Collection and is **not** production ready. |
|-----------------------------------------------------------------------------------------------------------------------|


This example provisions a simple static site using Linode Object Storage.

## Usage

In order to run this playbook, you must create a Linode [Personal Access Token](https://www.linode.com/docs/guides/getting-started-with-the-linode-api/#get-an-access-token).

While in the `obj_static_site` directory, run the following:

```bash
export LINODE_TOKEN=mytoken
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook deploy.yml
```

This will execute the playbook, including provisioning an Object Storage Bucket and configuring it to serve a static site.

After the playbook has finished running, the website should be accessible at the `Static Site Access URL` found in the playbook run logs. This URL will automatically resolve to the contents of `files/public/index.html`. If the requested URL is not found, the page will automatically resolve to the contents of `files/public/404.html`.

This example can be configured by editing the `config.yml` file. 

## Structure

- `config.yml` - Stores various configuration fields for this playbook.
- `deploy.yml` - The primary playbook file for this example. Calls out to roles to run provisioning steps.
- `roles`
  - `static_site`
    - `files`
      - `index.html` - The landing page for the static site.
      - `404.html` - The page to show users hitting a 404 response.
    - `tasks`
      - `main.yml` - Provisions a Linode Object Storage bucket, uploads the appropriate files, and configured the bucket as a static site.
  