.. _domain_info_module:


domain_info
===========

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode Domain.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------


  **domain (type=str):**
    \• The unique id of the Domain.


  **id (type=int):**
    \• The unique domain name of the Domain.







Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get info about a domain by domain
      linode.cloud.domain_info:
        domain: my-domain.com

    - name: Get info about a domain by id
      linode.cloud.domain_info:
        id: 12345




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

