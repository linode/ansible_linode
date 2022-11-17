# Linode Ansible Collection
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-linode.cloud-660198.svg?style=flat)](https://galaxy.ansible.com/linode/cloud/) 
![Build](https://img.shields.io/github/workflow/status/linode/ansible_linode/Run%20Integration%20Tests/main?label=tests)
![Code Quality](https://img.shields.io/lgtm/grade/python/github/linode/ansible_linode?label=code%20quality)

The Ansible Linode Collection contains various plugins for managing Linode services.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

<!--start collection content-->
### Modules

Modules for managing Linode infrastructure.

Name | Description |
--- | ------------ |
[linode.cloud.api_request](./docs/modules/api_request.md)|Make an arbitrary Linode API request.|
[linode.cloud.database_mysql](./docs/modules/database_mysql.md)|Manage a Linode MySQL database.|
[linode.cloud.database_postgresql](./docs/modules/database_postgresql.md)|Manage a Linode PostgreSQL database.|
[linode.cloud.domain](./docs/modules/domain.md)|Manage Linode Domains.|
[linode.cloud.domain_record](./docs/modules/domain_record.md)|Manage Linode Domain Records.|
[linode.cloud.firewall](./docs/modules/firewall.md)|Manage Linode Firewalls.|
[linode.cloud.firewall_device](./docs/modules/firewall_device.md)|Manage Linode Firewall Devices.|
[linode.cloud.image](./docs/modules/image.md)|Manage a Linode Image.|
[linode.cloud.instance](./docs/modules/instance.md)|Manage Linode Instances, Configs, and Disks.|
[linode.cloud.lke_cluster](./docs/modules/lke_cluster.md)|Manage Linode LKE clusters.|
[linode.cloud.lke_node_pool](./docs/modules/lke_node_pool.md)|Manage Linode LKE cluster node pools.|
[linode.cloud.nodebalancer](./docs/modules/nodebalancer.md)|Manage a Linode NodeBalancer.|
[linode.cloud.nodebalancer_node](./docs/modules/nodebalancer_node.md)|Manage Linode NodeBalancer Nodes.|
[linode.cloud.object_keys](./docs/modules/object_keys.md)|Manage Linode Object Storage Keys.|
[linode.cloud.stackscript](./docs/modules/stackscript.md)|Manage a Linode StackScript.|
[linode.cloud.token](./docs/modules/token.md)|Manage a Linode Token.|
[linode.cloud.user](./docs/modules/user.md)|Manage a Linode User.|
[linode.cloud.volume](./docs/modules/volume.md)|Manage a Linode Volume.|


### Info Modules

Modules for retrieving information about existing Linode infrastructure.

Name | Description |
--- | ------------ |
[linode.cloud.account_info](./docs/modules/account_info.md)|Get info about a Linode Account.|
[linode.cloud.database_mysql_info](./docs/modules/database_mysql_info.md)|Get info about a Linode MySQL Managed Database.|
[linode.cloud.database_postgresql_info](./docs/modules/database_postgresql_info.md)|Get info about a Linode PostgreSQL Managed Database.|
[linode.cloud.domain_info](./docs/modules/domain_info.md)|Get info about a Linode Domain.|
[linode.cloud.domain_record_info](./docs/modules/domain_record_info.md)|Get info about a Linode Domain Record.|
[linode.cloud.firewall_info](./docs/modules/firewall_info.md)|Get info about a Linode Firewall.|
[linode.cloud.image_info](./docs/modules/image_info.md)|Get info about a Linode Image.|
[linode.cloud.instance_info](./docs/modules/instance_info.md)|Get info about a Linode Instance.|
[linode.cloud.ip_info](./docs/modules/ip_info.md)|Get info about a Linode IP.|
[linode.cloud.ipv6_range_info](./docs/modules/ipv6_range_info.md)|Get info about a Linode IPv6 range.|
[linode.cloud.lke_cluster_info](./docs/modules/lke_cluster_info.md)|Get info about a Linode LKE cluster.|
[linode.cloud.nodebalancer_info](./docs/modules/nodebalancer_info.md)|Get info about a Linode NodeBalancer.|
[linode.cloud.object_cluster_info](./docs/modules/object_cluster_info.md)|Get info about a Linode Object Storage Cluster.|
[linode.cloud.profile_info](./docs/modules/profile_info.md)|Get info about a Linode Profile.|
[linode.cloud.stackscript_info](./docs/modules/stackscript_info.md)|Get info about a Linode StackScript.|
[linode.cloud.token_info](./docs/modules/token_info.md)|Get info about a Linode Personal Access Token.|
[linode.cloud.user_info](./docs/modules/user_info.md)|Get info about a Linode User.|
[linode.cloud.vlan_info](./docs/modules/vlan_info.md)|Get info about a Linode VLAN.|
[linode.cloud.volume_info](./docs/modules/volume_info.md)|Get info about a Linode Volume.|


### List Modules

Modules for retrieving and filtering on multiple Linode resources.

Name | Description |
--- | ------------ |
[linode.cloud.event_list](./docs/modules/event_list.md)|List and filter on Linode events.|
[linode.cloud.image_list](./docs/modules/image_list.md)|List and filter on Linode images.|
[linode.cloud.stackscript_list](./docs/modules/stackscript_list.md)|List and filter on Linode stackscripts.|
[linode.cloud.vlan_list](./docs/modules/vlan_list.md)|List and filter on Linode VLANs.|


### Inventory Plugins

Dynamically add Linode infrastructure to an Ansible inventory.

Name |
--- |
[linode.cloud.instance](./docs/inventory/instance.rst)|


<!--end collection content-->

## Installation

You can install the Linode collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install linode.cloud
```

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```shell
pip install -r requirements.txt
```

## Usage
Once the Linode Ansible collection is installed, it can be referenced by its [Fully Qualified Collection Namespace (FQCN)](https://github.com/ansible-collections/overview#terminology): `linode.cloud.module_name`.

In order to use this collection, the `LINODE_API_TOKEN` environment variable must be set to a valid Linode API v4 token. 
Alternatively, you can pass your Linode API v4 token into the `api_token` option for each Linode module you reference.

The `LINODE_UA_PREFIX` or the `ua_prefix` module option can be used to specify a custom User-Agent prefix.

#### Example Playbook
```yaml
---
- name: create linode instance
  hosts: localhost
  tasks:
    - name: Create a Linode instance    
      linode.cloud.instance:
        label: my-linode
        type: g6-nanode-1
        region: us-east
        image: linode/ubuntu20.04
        root_pass: verysecurepassword!!!
        state: present
```

For more information on Ansible collection usage, see [Ansible's official usage guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## Examples

Use-case examples for this collection can be found [here](./examples/README.md).

## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.
