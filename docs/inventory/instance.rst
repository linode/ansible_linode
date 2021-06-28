.. _instance_module:


instance
========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Reads instance inventories from Linode.

Uses a YAML configuration file that ends with linode.(yml|yaml).

Linode labels are used by default as the hostnames.

The default inventory groups are built from groups (deprecated by Linode) and not tags.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 2.0.0



Parameters
----------

  plugin (True, any, None)
    marks this as an instance of the 'linode' plugin


  api_token (True, any, None)
    The Linode account personal access token.


  regions (optional, list, [])
    Populate inventory with instances in this region.


  tags (optional, list, [])
    Populate inventory only with instances which have at least one of the tags listed here.


  types (optional, list, [])
    Populate inventory with instances with this type.


  strict (optional, bool, False)
    If ``yes`` make invalid entries a fatal error, otherwise skip and continue.

    Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


  compose (optional, dict, {})
    Create vars from jinja2 expressions.


  groups (optional, dict, {})
    Add hosts to group based on Jinja2 conditionals.


  keyed_groups (optional, list, [])
    Add hosts to group based on the values of a variable.


  use_extra_vars (optional, bool, False)
    Merge extra vars into the available variables for composition (highest precedence).


  leading_separator (optional, boolean, True)
    Use in conjunction with keyed_groups.

    By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

    This is because the default prefix is "" and the default separator is "_".

    Set this option to False to omit the leading underscore (or other separator) if no prefix is given.

    If the group name is derived from a mapping the separator is still used to concatenate the items.

    To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.









Examples
--------

.. code-block:: yaml+jinja

    
    # Minimal example. `LINODE_API_TOKEN` is exposed in environment.
    plugin: linode.cloud.instance

    # Example with regions, types, groups and access token
    plugin: linode.cloud.instance
    api_token: foobar
    regions:
      - eu-west
    types:
      - g5-standard-2

    # Example with keyed_groups, groups, and compose
    plugin: linode.cloud.instance
    api_token: foobar
    keyed_groups:
      - key: tags
        separator: ''
      - key: region
        prefix: region
    groups:
      webservers: "'web' in (tags|list)"
      mailservers: "'mail' in (tags|list)"
    compose:
      ansible_port: 2222






Status
------





Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Lena Garber (@LBGarber)

