.. _object_cluster_info_module:


object_cluster_info
===================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get info about a Linode Object Storage Cluster.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3



Parameters
----------


  **domain (type=str):**
    \• The domain of the clusters.


  **id (type=str):**
    \• The unique id given to the clusters.


  **region (type=str):**
    \• The region the clusters are in.


  **static_site_domain (type=str):**
    \• The static-site domain of the clusters.







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

**clusters (returned=always, type=list):**

The Object Storage clusters in JSON serialized form.

`Linode Response Object Documentation <https://www.linode.com/docs/api/object-storage/#cluster-view__responses>`_

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

