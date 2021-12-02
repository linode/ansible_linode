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

- python >= 3
- linode_api4 >= 2.0.0



Parameters
----------

  **plugin (required=True, type=any, default=None):**
    \• Marks this as an instance of the 'linode' plugin


  **api_token (required=True, type=any, default=None):**
    \• The Linode account personal access token.


  **regions (required=optional, type=list, default=[]):**
    \• Populate inventory with instances in this region.


  **tags (required=optional, type=list, default=[]):**
    \• Populate inventory only with instances which have at least one of the tags listed here.


  **types (required=optional, type=list, default=[]):**
    \• Populate inventory with instances with this type.


  **strict (required=optional, type=bool, default=False):**
    \• If ``yes`` make invalid entries a fatal error, otherwise skip and continue.

    \• Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


  **compose (required=optional, type=dict, default={}):**
    \• Create vars from jinja2 expressions.


  **groups (required=optional, type=dict, default={}):**
    \• Add hosts to group based on Jinja2 conditionals.


  **keyed_groups (required=optional, type=list, default=[]):**
    \• Add hosts to group based on the values of a variable.


      **parent_group (required=optional, type=str, default=None):**
        \• parent group for keyed group


      **prefix (required=optional, type=str, default=):**
        \• A keyed group name will start with this prefix


      **separator (required=optional, type=str, default=_):**
        \• separator used to build the keyed group name


      **key (required=optional, type=str, default=None):**
        \• The key from input dictionary used to generate groups


      **default_value (required=optional, type=str, default=None):**
        \• The default value when the host variable's value is an empty string.

        \• This option is mutually exclusive with ``trailing_separator``.


      **trailing_separator (required=optional, type=bool, default=True):**
        \• Set this option to *False* to omit the ``separator`` after the host variable when the value is an empty string.

        \• This option is mutually exclusive with ``default_value``.



  **use_extra_vars (required=optional, type=bool, default=False):**
    \• Merge extra vars into the available variables for composition (highest precedence).


  **leading_separator (required=optional, type=boolean, default=True):**
    \• Use in conjunction with keyed_groups.

    \• By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

    \• This is because the default prefix is "" and the default separator is "_".

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

