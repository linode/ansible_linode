.. _domain_record_module:


domain_record
=============

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Linode Domain Records.



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


  label (False, str, None)

  name (True, str, None)
    The name of this Record.


  port (False, int, None)
    The port this Record points to.

    Only valid and required for SRV record requests.


  priority (False, int, None)
    The priority of the target host for this Record.

    Lower values are preferred.

    Only valid for MX and SRV record requests.

    Required for SRV record requests.


  protocol (False, str, None)
    The protocol this Record’s service communicates with.

    An underscore (_) is prepended automatically to the submitted value for this property.


  service (False, str, None)
    An underscore (_) is prepended and a period (.) is appended automatically to the submitted value for this property.

    Only valid and required for SRV record requests.

    The name of the service.


  tag (False, str, None)
    The tag portion of a CAA record.

    Only valid and required for CAA record requests.


  target (False, str, None)
    The target for this Record.


  ttl_sec (False, int, None)
    The amount of time in seconds that this Domain’s records may be cached       by resolvers or other domain servers.


  type (False, str, None)
    The type of Record this is in the DNS system.


  weight (False, int, None)
    The relative weight of this Record used in the case of identical priority.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a A record
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

