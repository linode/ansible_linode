# MySQL/Adminer Deployment Example

| This example is intended to provide usage examples for the Linode Ansible Collection and is **not** production ready. |
|-----------------------------------------------------------------------------------------------------------------------|

This example provisions a MySQL/Adminer setup using two Linode instances attached to a VLAN, a Linode Firewall, and a Linode Volume. 

## Usage

In order to run this playbook, you must create a Linode [Personal Access Token](https://www.linode.com/docs/guides/getting-started-with-the-linode-api/#get-an-access-token).

While in the `mysql_adminer` directory, run the following:

```bash
export LINODE_TOKEN=mytoken
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook deploy.yml
```

This will execute the playbook, including provisioning the necessary infrastructure and configuring each new node.

Once the playbook has finished executing, the Adminer interface can be accessed through the `Adminer Access URL` field in the playbook run output. 

The root MySQL user can be logged into using the following credentials:

`Username` - `root`

`Password` - The value of `mysql_root_password` in `config.yml`

This example can be configured by editing the `config.yml` file. 

## Structure

- `config.yml` - Stores various configuration fields for this playbook.
- `deploy.yml` - The primary playbook file for this example. Calls out to roles to run provisioning steps.
- `roles`
  - `infra`
    - `tasks`
      - `main.yml` - The entrypoint for this role.
      - `instances.yml` - Provisions the Linode instances for this deployment.
      - `firewall.yml` - Provisions the Linode Firewall to sit in front of the Linode instances.
      - `volume.yml` - Provisions a Linode volume to be attached to the `mysql` instance.
  - `configure_mysql`
    - `tasks`
      - `main.yml` - The entrypoint for this role.
      - `volume_mount.yml` - Mounts and formats the attached volume.
      - `configure_mysql.yml` - Installs docker on the host and deploys `mysql:latest`.