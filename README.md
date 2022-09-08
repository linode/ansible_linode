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
Name |
--- |
[linode.cloud.account_info](./docs/modules/account_info.md)|
[linode.cloud.domain](./docs/modules/domain.md)|
[linode.cloud.domain_info](./docs/modules/domain_info.md)|
[linode.cloud.domain_record](./docs/modules/domain_record.md)|
[linode.cloud.domain_record_info](./docs/modules/domain_record_info.md)|
[linode.cloud.firewall](./docs/modules/firewall.md)|
[linode.cloud.firewall_device](./docs/modules/firewall_device.md)|
[linode.cloud.firewall_info](./docs/modules/firewall_info.md)|
[linode.cloud.instance](./docs/modules/instance.md)|
[linode.cloud.instance_info](./docs/modules/instance_info.md)|
[linode.cloud.lke_cluster](./docs/modules/lke_cluster.md)|
[linode.cloud.lke_cluster_info](./docs/modules/lke_cluster_info.md)|
[linode.cloud.lke_node_pool](./docs/modules/lke_node_pool.md)|
[linode.cloud.nodebalancer](./docs/modules/nodebalancer.md)|
[linode.cloud.nodebalancer_info](./docs/modules/nodebalancer_info.md)|
[linode.cloud.nodebalancer_node](./docs/modules/nodebalancer_node.md)|
[linode.cloud.object_cluster_info](./docs/modules/object_cluster_info.md)|
[linode.cloud.object_keys](./docs/modules/object_keys.md)|
[linode.cloud.profile_info](./docs/modules/profile_info.md)|
[linode.cloud.stackscript](./docs/modules/stackscript.md)|
[linode.cloud.token](./docs/modules/token.md)|
[linode.cloud.vlan_info](./docs/modules/vlan_info.md)|
[linode.cloud.volume](./docs/modules/volume.md)|
[linode.cloud.volume_info](./docs/modules/volume_info.md)|


### Inventory
Name |
--- |
[linode.cloud.instance](./docs/inventory/instance.md)|


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