# Linode Ansible Collection
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
Name | Description
--- | ---
[linode.cloud.firewall](https://github.com/linode/ansible_linode/blob/master/docs/firewall.rst)|Create and destroy Firewalls.
[linode.cloud.firewall_info](https://github.com/linode/ansible_linode/blob/master/docs/firewall_info.rst)|Gather info about an existing Firewall.
[linode.cloud.instance](https://github.com/linode/ansible_linode/blob/master/docs/instance.rst)|Create and destroy Linodes.
[linode.cloud.instance_info](https://github.com/linode/ansible_linode/blob/master/docs/instance_info.rst)|Gather info about an existing Linode instance.
[linode.cloud.nodebalancer](https://github.com/linode/ansible_linode/blob/master/docs/nodebalancer.rst)|Create, destroy, and configure NodeBalancers.
[linode.cloud.nodebalancer_info](https://github.com/linode/ansible_linode/blob/master/docs/nodebalancer_info.rst)|Gather info about an existing NodeBalancer.
[linode.cloud.object_cluster_info](https://github.com/linode/ansible_linode/blob/master/docs/object_cluster_info.rst)|Gather info about Object Storage clusters.
[linode.cloud.object_keys](https://github.com/linode/ansible_linode/blob/master/docs/object_keys.rst)|Create and destroy Object Storage keys.
[linode.cloud.vlan_info](https://github.com/linode/ansible_linode/blob/master/docs/vlan_info.rst)|Gather info about an existing Linode VLAN.
[linode.cloud.volume](https://github.com/linode/ansible_linode/blob/master/docs/volume.rst)|Create, destroy, and attach Linode volumes.
[linode.cloud.volume_info](https://github.com/linode/ansible_linode/blob/master/docs/volume_info.rst)|Gather info about an existing Linode volume.

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

## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.