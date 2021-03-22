.. _object_cluster_info_module:


object_cluster_info
===================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get information about an Object Storage cluster.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 2.7
- linode_api4 >= 3.0



Parameters
----------

  id (optional, string, None)
    The unique id given to the clusters


  region (optional, string, None)
    The region the clusters are in


  domain (optional, string, None)
    The domain of the clusters


  static_site_domain (optional, string, None)
    The static-site domain of the clusters









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get info about clusters in us-east
      linode.cloud.object_cluster_info:
        region: us-east

    - name: Get info about the cluster with id us-east-1
      linode.cloud.object_cluster_info:
        id: us-east-1




Return Values
-------------

clusters (always, list):

The Object Storage clusters in JSON serialized form.

Sample Response:

.. code-block:: JSON

    [
     {
      "domain": "us-east-1.linodeobjects.com",
      "id": "us-east-1",
      "region": "us-east",
      "static_site_domain": "website-us-east-1.linodeobjects.com",
      "status": "available"
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

