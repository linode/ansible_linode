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


  **domain (type=str):**
    \• The name of the parent Domain.


  **domain_id (type=int):**
    \• The ID of the parent Domain.


  **label (type=str):**

  **name (type=str):**
    \• The name of this Record.


  **port (type=int):**
    \• The port this Record points to.

    \• Only valid and required for SRV record requests.


  **priority (type=int):**
    \• The priority of the target host for this Record.

    \• Lower values are preferred.

    \• Only valid for MX and SRV record requests.

    \• Required for SRV record requests.


  **protocol (type=str):**
    \• The protocol this Record’s service communicates with.

    \• An underscore (_) is prepended automatically to the submitted value for this property.


  **record_id (type=int):**
    \• The id of the record to modify.


  **service (type=str):**
    \• An underscore (_) is prepended and a period (.) is appended automatically to the submitted value for this property.

    \• Only valid and required for SRV record requests.

    \• The name of the service.


  **tag (type=str):**
    \• The tag portion of a CAA record.

    \• Only valid and required for CAA record requests.


  **target (type=str):**
    \• The target for this Record.


  **ttl_sec (type=int):**
    \• The amount of time in seconds that this Domain’s records may be cached       by resolvers or other domain servers.


  **type (type=str):**
    \• The type of Record this is in the DNS system.


  **weight (type=int):**
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
- Jacob Riddle (@jriddle)

