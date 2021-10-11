.. _domain_module:


domain
======

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Domains.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------

  **axfr_ips (required=False, type=list, default=None):**
    \• The list of IPs that may perform a zone transfer for this Domain.


  **description (required=False, type=str, default=None):**
    \• The list of IPs that may perform a zone transfer for this Domain.


  **domain (required=True, type=str, default=None):**
    \• The domain this Domain represents.


  **expire_sec (required=False, type=int, default=None):**
    \• The amount of time in seconds that may pass before this Domain is no longer authoritative.


  **master_ips (required=False, type=list, default=None):**
    \• The IP addresses representing the master DNS for this Domain.


  **refresh_sec (required=False, type=int, default=None):**
    \• The amount of time in seconds before this Domain should be refreshed.


  **retry_sec (required=False, type=int, default=None):**
    \• The interval, in seconds, at which a failed refresh should be retried.


  **soa_email (required=False, type=str, default=None):**
    \• The Start of Authority email address.


  **status (required=False, type=str, default=None):**
    \• Used to control whether this Domain is currently being rendered.


  **tags (required=False, type=list, default=None):**
    \• An array of tags applied to this object.


  **ttl_sec (required=False, type=int, default=None):**
    \• the amount of time in seconds that this Domain’s records may       be cached by resolvers or other domain servers.


  **type (required=False, type=str, default=None):**
    \• Whether this Domain represents the authoritative source of information for the domain it describes (master), or whether it is a read-only copy of a master (slave).







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a domain 
      linode.cloud.domain:
        domain: my-domain.com
        type: master
        state: present

    - name: Delete a domain
      linode.cloud.domain:
        domain: my-domain.com
        state: absent




Return Values
-------------

**domain (returned=always, type=dict):**

The domain in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/domains/#domain-view>`_

Sample Response:

.. code-block:: JSON

    {
     "axfr_ips": [],
     "created": "xxxx",
     "description": "Created with ansible!",
     "domain": "my-domain.com",
     "expire_sec": 300,
     "group": "",
     "id": "xxxxxx",
     "master_ips": [
      "127.0.0.1"
     ],
     "refresh_sec": 3600,
     "retry_sec": 7200,
     "soa_email": "xxxx@my-domain.com",
     "status": "active",
     "tags": [],
     "ttl_sec": 14400,
     "type": "master",
     "updated": "xxxx"
    }


**records (returned=always, type=list):**

A list of records associated with the domain in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/domains/#domain-record-view>`_

Sample Response:

.. code-block:: JSON

    [
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
    ]





Status
------




- This module is maintained by Linode.



Authors
~~~~~~~

- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)

