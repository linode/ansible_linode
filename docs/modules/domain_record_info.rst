.. _domain_record_info_module:


domain_record_info
==================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode Domain Records.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.0



Parameters
----------

  domain (False, str, None)
    The name of the parent Domain.


  domain_id (False, int, None)
    The ID of the parent Domain.


  id (False, int, None)
    The unique id of the subdomain.


  name (False, str, None)
    The name of the subdomain.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get info about a domain record by name
      linode.cloud.domain_record_info:
        domain: my-domain.com
        name: my-subdomain

    - name: Get info about a domain record by id
      linode.cloud.domain_info:
        domain: my-domain.com
        id: 12345




Return Values
-------------

**record (always, dict):**

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

