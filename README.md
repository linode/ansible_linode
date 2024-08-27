# Linode Ansible Collection
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-linode.cloud-660198.svg?style=flat)](https://galaxy.ansible.com/linode/cloud/) 
![Tests](https://img.shields.io/github/actions/workflow/status/linode/ansible_linode/integration-tests.yml?branch=main)

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
[linode.cloud.ip_assign](./docs/modules/ip_assign.md)|Assign IPs to Linodes in a given Region.|
[linode.cloud.ip_rdns](./docs/modules/ip_rdns.md)|Manage a Linode IP address's rDNS.|
[linode.cloud.ip_share](./docs/modules/ip_share.md)|Manage the Linode shared IPs.|
[linode.cloud.lke_cluster](./docs/modules/lke_cluster.md)|Manage Linode LKE clusters.|
[linode.cloud.lke_node_pool](./docs/modules/lke_node_pool.md)|Manage Linode LKE cluster node pools.|
[linode.cloud.nodebalancer](./docs/modules/nodebalancer.md)|Manage a Linode NodeBalancer.|
[linode.cloud.nodebalancer_node](./docs/modules/nodebalancer_node.md)|Manage Linode NodeBalancer Nodes.|
[linode.cloud.nodebalancer_stats](./docs/modules/nodebalancer_stats.md)|Get info about a Linode Node Balancer Stats.|
[linode.cloud.object_keys](./docs/modules/object_keys.md)|Manage Linode Object Storage Keys.|
[linode.cloud.placement_group](./docs/modules/placement_group.md)|Manage a Linode Placement Group.|
[linode.cloud.placement_group_assign](./docs/modules/placement_group_assign.md)|Manages a single assignment between a Linode and a Placement Group.|
[linode.cloud.ssh_key](./docs/modules/ssh_key.md)|Manage a Linode SSH key.|
[linode.cloud.stackscript](./docs/modules/stackscript.md)|Manage a Linode StackScript.|
[linode.cloud.token](./docs/modules/token.md)|Manage a Linode Token.|
[linode.cloud.user](./docs/modules/user.md)|Manage a Linode User.|
[linode.cloud.volume](./docs/modules/volume.md)|Manage a Linode Volume.|
[linode.cloud.vpc](./docs/modules/vpc.md)|Create, read, and update a Linode VPC.|
[linode.cloud.vpc_subnet](./docs/modules/vpc_subnet.md)|Create, read, and update a Linode VPC Subnet.|


### Info Modules

Modules for retrieving information about existing Linode infrastructure.

Name | Description |
--- | ------------ |
[linode.cloud.account_availability_info](./docs/modules/account_availability_info.md)|Get info about a Linode Account Availability.|
[linode.cloud.account_info](./docs/modules/account_info.md)|Get info about a Linode Account.|
[linode.cloud.child_account_info](./docs/modules/child_account_info.md)|Get info about a Linode Child Account.|
[linode.cloud.database_mysql_info](./docs/modules/database_mysql_info.md)|Get info about a Linode MySQL Managed Database.|
[linode.cloud.database_postgresql_info](./docs/modules/database_postgresql_info.md)|Get info about a Linode PostgreSQL Managed Database.|
[linode.cloud.domain_info](./docs/modules/domain_info.md)|Get info about a Linode Domain.|
[linode.cloud.domain_record_info](./docs/modules/domain_record_info.md)|Get info about a Linode Domain Records.|
[linode.cloud.firewall_info](./docs/modules/firewall_info.md)|Get info about a Linode Firewall.|
[linode.cloud.image_info](./docs/modules/image_info.md)|Get info about a Linode Image.|
[linode.cloud.instance_info](./docs/modules/instance_info.md)|Get info about a Linode Instance.|
[linode.cloud.ip_info](./docs/modules/ip_info.md)|Get info about a Linode IP.|
[linode.cloud.ipv6_range_info](./docs/modules/ipv6_range_info.md)|Get info about a Linode IPv6 range.|
[linode.cloud.lke_cluster_info](./docs/modules/lke_cluster_info.md)|Get info about a Linode LKE cluster.|
[linode.cloud.nodebalancer_info](./docs/modules/nodebalancer_info.md)|Get info about a Linode Node Balancer.|
[linode.cloud.object_cluster_info](./docs/modules/object_cluster_info.md)|**NOTE: This module has been deprecated because it relies on deprecated API endpoints. Going forward, `region` will be the preferred way to designate where Object Storage resources should be created.**|
[linode.cloud.placement_group_info](./docs/modules/placement_group_info.md)|Get info about a Linode Placement Group.|
[linode.cloud.profile_info](./docs/modules/profile_info.md)|Get info about a Linode Profile.|
[linode.cloud.ssh_key_info](./docs/modules/ssh_key_info.md)|Get info about the Linode SSH public key.|
[linode.cloud.stackscript_info](./docs/modules/stackscript_info.md)|Get info about a Linode StackScript.|
[linode.cloud.token_info](./docs/modules/token_info.md)|Get info about a Linode Personal Access Token.|
[linode.cloud.type_info](./docs/modules/type_info.md)|Get info about a Linode Type.|
[linode.cloud.user_info](./docs/modules/user_info.md)|Get info about a Linode User.|
[linode.cloud.vlan_info](./docs/modules/vlan_info.md)|Get info about a Linode VLAN.|
[linode.cloud.volume_info](./docs/modules/volume_info.md)|Get info about a Linode Volume.|
[linode.cloud.vpc_info](./docs/modules/vpc_info.md)|Get info about a Linode VPC.|
[linode.cloud.vpc_subnet_info](./docs/modules/vpc_subnet_info.md)|Get info about a Linode VPC Subnet.|


### List Modules

Modules for retrieving and filtering on multiple Linode resources.

Name | Description |
--- | ------------ |
[linode.cloud.account_availability_list](./docs/modules/account_availability_list.md)|List and filter on Account Availabilities.|
[linode.cloud.child_account_list](./docs/modules/child_account_list.md)|List and filter on Child Account.|
[linode.cloud.database_engine_list](./docs/modules/database_engine_list.md)|List and filter on Managed Database engine types.|
[linode.cloud.database_list](./docs/modules/database_list.md)|List and filter on Linode Managed Databases.|
[linode.cloud.domain_list](./docs/modules/domain_list.md)|List and filter on Domains.|
[linode.cloud.event_list](./docs/modules/event_list.md)|List and filter on Events.|
[linode.cloud.firewall_list](./docs/modules/firewall_list.md)|List and filter on Firewalls.|
[linode.cloud.image_list](./docs/modules/image_list.md)|List and filter on Images.|
[linode.cloud.instance_list](./docs/modules/instance_list.md)|List and filter on Instances.|
[linode.cloud.instance_type_list](./docs/modules/instance_type_list.md)|**NOTE: This module has been deprecated in favor of `type_list`.|
[linode.cloud.lke_version_list](./docs/modules/lke_version_list.md)|List Kubernetes versions available for deployment to a Kubernetes cluster.|
[linode.cloud.nodebalancer_list](./docs/modules/nodebalancer_list.md)|List and filter on Node Balancers.|
[linode.cloud.object_cluster_list](./docs/modules/object_cluster_list.md)|**NOTE: This module has been deprecated because it relies on deprecated API endpoints. Going forward, `region` will be the preferred way to designate where Object Storage resources should be created.**|
[linode.cloud.placement_group_list](./docs/modules/placement_group_list.md)|List and filter on Placement Groups.|
[linode.cloud.region_list](./docs/modules/region_list.md)|List and filter on Regions.|
[linode.cloud.ssh_key_list](./docs/modules/ssh_key_list.md)|List and filter on SSH keys in the Linode profile.|
[linode.cloud.stackscript_list](./docs/modules/stackscript_list.md)|List and filter on StackScripts.|
[linode.cloud.token_list](./docs/modules/token_list.md)|List and filter on Tokens.|
[linode.cloud.type_list](./docs/modules/type_list.md)|List and filter on Types.|
[linode.cloud.user_list](./docs/modules/user_list.md)|List Users.|
[linode.cloud.vlan_list](./docs/modules/vlan_list.md)|List and filter on Linode VLANs.|
[linode.cloud.volume_list](./docs/modules/volume_list.md)|List and filter on Linode Volumes.|
[linode.cloud.vpc_ip_list](./docs/modules/vpc_ip_list.md)|List and filter on VPC IP Addresses.|
[linode.cloud.vpc_list](./docs/modules/vpc_list.md)|List and filter on VPCs.|
[linode.cloud.vpc_subnet_list](./docs/modules/vpc_subnet_list.md)|List and filter on VPC Subnets.|
[linode.cloud.vpcs_ip_list](./docs/modules/vpcs_ip_list.md)|List and filter on all VPC IP Addresses.|


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

The Python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```shell
pip install --upgrade -r https://raw.githubusercontent.com/linode/ansible_linode/main/requirements.txt
```

> :warning: **NOTE:** Python dependencies should always be reinstalled when upgrading collection versions

## Usage
Once the Linode Ansible collection is installed, it can be referenced by its [Fully Qualified Collection Namespace (FQCN)](https://github.com/ansible-collections/overview#terminology): `linode.cloud.module_name`.

In order to use this collection, the `LINODE_API_TOKEN` environment variable must be set to a valid Linode API v4 token. 
Alternatively, you can pass your Linode API v4 token into the `api_token` option for each Linode module you reference.

The `LINODE_UA_PREFIX` environment variable or the `ua_prefix` module option can be used to specify a custom User-Agent prefix.

The `LINODE_API_URL` environment variable pr the `api_url` module option can be used to specify a custom API base url.

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
        image: linode/ubuntu22.04
        root_pass: verysecurepassword!!!
        state: present
```

For more information on Ansible collection usage, see [Ansible's official usage guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## Examples

Use-case examples for this collection can be found [here](./examples/README.md).

## Development

The following section outlines various information relating to the development of this collection.

### Attaching a Debugger

To quickly and easily attach a debugger to a running module in this collection, 
you can use the [madbg](https://pypi.org/project/madbg/) package:

1. Install `madbg` in your local Python environment:

```shell
pip install madbg
```

2. Call `madbg.set_trace(...)` at the location you would like to create a breakpoint at:

```shell
import madbg; madbg.set_trace()
```

3. Run the module in either a playbook or a test.
4. In a separate shell, run `madbg connect`.
5. You should now be able to remotely debug the module as soon as the breakpoint is triggered.

## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.