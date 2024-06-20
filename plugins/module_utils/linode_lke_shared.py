"""
Contains shared helper functions related to LKE.
"""

from typing import Any, Dict, Optional

from linode_api4 import ApiError, LKECluster


def safe_get_cluster_acl(cluster: LKECluster) -> Optional[Dict[str, Any]]:
    """
    Gets the control plane ACL configuration of a cluster, returning None
    if the user does not currently have access to LKE ACLs.
    """
    # Invalidate the cached ACL
    cluster.invalidate()

    try:
        return cluster.control_plane_acl.dict
    except ApiError as err:
        if err.status not in (404, 400):
            raise err

    return None
