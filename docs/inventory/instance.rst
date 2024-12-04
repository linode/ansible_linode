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

- python \>= 3
- linode\_api4 \>= 2.0.0



Parameters
----------

  **plugin (Required, type=any):**
    \• Marks this as an instance of the 'linode' plugin

    \• Options: `linode`, `linode.cloud.instance`


  **api_token (Required, type=any):**
    \• The Linode account personal access token.



  **regions (type=list):**
    \• Populate inventory with instances in this region.


  **tags (type=list):**
    \• Populate inventory only with instances which have at least one of the tags listed here.


  **types (type=list):**
    \• Populate inventory with instances with this type.


  **strict (type=bool):**
    \• If \ :literal:`yes`\  make invalid entries a fatal error, otherwise skip and continue.

    \• Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


  **compose (type=dict):**
    \• Create vars from jinja2 expressions.


  **groups (type=dict):**
    \• Add hosts to group based on Jinja2 conditionals.


  **keyed_groups (type=list):**
    \• Add hosts to group based on the values of a variable.


      **parent_group (type=str):**
        \• parent group for keyed group


      **prefix (type=str):**
        \• A keyed group name will start with this prefix


      **separator (type=str, default=_):**
        \• separator used to build the keyed group name


      **key (type=str):**
        \• The key from input dictionary used to generate groups


      **default_value (type=str):**
        \• The default value when the host variable's value is an empty string.

        \• This option is mutually exclusive with \ :literal:`keyed\_groups[].trailing\_separator`\ .


      **trailing_separator (type=bool, default=True):**
        \• Set this option to \ :literal:`False`\  to omit the \ :literal:`keyed\_groups[].separator`\  after the host variable when the value is an empty string.

        \• This option is mutually exclusive with \ :literal:`keyed\_groups[].default\_value`\ .



  **use_extra_vars (type=bool):**
    \• Merge extra vars into the available variables for composition (highest precedence).


  **leading_separator (type=boolean, default=True):**
    \• Use in conjunction with keyed\_groups.

    \• By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

    \• This is because the default prefix is "" and the default separator is "\_".

    \• Set this option to False to omit the leading underscore (or other separator) if no prefix is given.

    \• If the group name is derived from a mapping the separator is still used to concatenate the items.

    \• To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.







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

