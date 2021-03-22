# Linode Ansible Collection
The Ansible Linode Collection contains various plugins for managing Linode services.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Installation

You can install the Linode collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install linode.cloud

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

    pip install -r requirements.txt

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

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.