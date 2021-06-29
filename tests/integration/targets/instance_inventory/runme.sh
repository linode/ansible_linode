#!/usr/bin/env bash

#set -eux

# Create testing instance
ansible-playbook playbooks/setup_instance.yml "$@"

# Test an inventory with no filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=nofilter.instance.yml" "$@"
ANSIBLE_INVENTORY=nofilter.instance.yml ansible-playbook playbooks/test_inventory_nofilter.yml "$@"

# Test an inventory with a filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=filter.instance.yml" "$@"
ANSIBLE_INVENTORY=filter.instance.yml ansible-playbook playbooks/test_inventory_filter.yml "$@"

# Clean up
ansible-playbook playbooks/teardown.yml "$@"