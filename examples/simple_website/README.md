# Simple Website Example

| This example is intended to provide usage examples for the Linode Ansible Collection and is **not** production ready. |
|-----------------------------------------------------------------------------------------------------------------------|

This example provisions three Linode Instances and deploys a load-balanced HTTP server.

## Usage

In order to run this playbook, you must create a Linode [Personal Access Token](https://www.linode.com/docs/guides/getting-started-with-the-linode-api/#get-an-access-token).

While in the `simple_website` directory, run the following:

```bash
export LINODE_TOKEN=mytoken
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook deploy.yml
```

This will execute the playbook, including provisioning the necessary infrastructure and configuring each new node.


Once the playbook has finished executing, visit the [NodeBalancers](https://cloud.linode.com/nodebalancers) page in the Linode Cloud Manager. If the playbook ran successfully, a new NodeBalancer should be created with a single configuration on port 80 with three backend nodes.

In order to access the deployed app, visit the IP address exposed by the NodeBalancer.

This example can be configured by editing the `config.yml` file. 

## Structure

- `config.yml` - Stores various configuration fields for this playbook.
- `deploy.yml` - The primary playbook file for this example. Calls out to roles to run provisioning steps.
- `roles`
  - `infra`
    - `tasks`
      - `main.yml` - Provisions the Linode infrastructure for this playbook (3 Instances, 1 NodeBalancer)
  - `website`
    - `tasks`
      - `main.yml` - Deploys the HTTP application to each individual node. This role specifically deploys Docker and runs the [`httpd`](https://hub.docker.com/_/httpd) Docker image.