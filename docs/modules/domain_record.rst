.. _domain_record_module:


domain_record
=============

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Domain Records.

NOTE: Domain records are identified by their name, target, and type.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **domain (required=False, type=str, default=None):**
    \• The name of the parent Domain.


  **domain_id (required=False, type=int, default=None):**
    \• The ID of the parent Domain.


  **label (required=False, type=str, default=None):**

  **name (required=False, type=str, default=None):**
    \• The name of this Record.


  **port (required=False, type=int, default=None):**
    \• The port this Record points to.

    \• Only valid and required for SRV record requests.


  **priority (required=False, type=int, default=None):**
    \• The priority of the target host for this Record.

    \• Lower values are preferred.

    \• Only valid for MX and SRV record requests.

    \• Required for SRV record requests.


  **protocol (required=False, type=str, default=None):**
    \• The protocol this Record’s service communicates with.

    \• An underscore (_) is prepended automatically to the submitted value for this property.


  **record_id (required=False, type=int, default=None):**
    \• The id of the record to modify.


  **service (required=False, type=str, default=None):**
    \• An underscore (_) is prepended and a period (.) is appended automatically to the submitted value for this property.

    \• Only valid and required for SRV record requests.

    \• The name of the service.


  **tag (required=False, type=str, default=None):**
    \• The tag portion of a CAA record.

    \• Only valid and required for CAA record requests.


  **target (required=False, type=str, default=):**
    \• The target for this Record.


  **ttl_sec (required=False, type=int, default=None):**
    \• The amount of time in seconds that this Domain’s records may be cached       by resolvers or other domain servers.


  **type (required=False, type=str, default=None):**
    \• The type of Record this is in the DNS system.


  **weight (required=False, type=int, default=None):**
    \• The relative weight of this Record used in the case of identical priority.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create an A record
      linode.cloud.domain_record:
        domain: my-domain.com
        name: my-subdomain
        type: 'A'
        target: '127.0.0.1'
        state: present

    - name: Delete a domain record
      linode.cloud.domain:
        domain: my-domain.com
        name: my-subdomain
        state: absent




Return Values
-------------

**record (returned=always, type=dict):**

The domain record in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/domains/#domain-record-view>`_

Sample Response:

.. code-block:: JSON

    {
     "created": "xxxxx",
     "id": "xxxxx",
     "name": "xxxx",
     "port": 0,
     "priority": 0,
     "protocol": null,
     "service": null,
     "tag": null,
     "target": "127.0.0.1",
     "ttl_sec": 3600,
     "type": "A",
     "updated": "xxxxx",
     "weight": 55
    }





Status
------




- This module is maintained by Linode.



Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)

