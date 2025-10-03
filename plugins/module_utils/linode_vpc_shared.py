"""
This file contains various helpers shared between VPC-related modules.
"""

from linode_api4 import VPCSubnet


def should_retry_subnet_delete_400s(
    client: "LinodeClient",
    subnet: VPCSubnet,
) -> bool:
    """
    Returns whether the given subnet should be retried upon a 400 error.

    This is necessary because database deletions and detachments can
    occasionally take longer than expected to propagate on VPC subnets.
    """

    # TODO: Use without _raw_json after support added to linode_api4
    subnet._api_get()

    subnet_dbs = {db.id: db for db in subnet._raw_json.get("databases", [])}
    if len(subnet_dbs) < 1:
        # Nothing to do here
        return False

    for db in client.database.instances():
        if db.private_network is None or db.private_network.id != subnet.id:
            continue

        subnet_dbs.pop(db.id)

    return len(subnet_dbs) < 1
