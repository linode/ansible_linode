"""
This file contains various helpers shared between VPC-related modules.
"""

from itertools import chain

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

    account_dbs = {
        db.id: db
        for db in chain(
            client.database.mysql_instances(),
            client.database.postgresql_instances(),
        )
    }

    if len(subnet.databases) < 1:
        # There are no databases attached to this subnet,
        # so there is nothing to retry
        return False

    for subnet_db in subnet.databases:
        if subnet_db.id not in account_dbs:
            continue

        db = account_dbs[subnet_db.id]
        db._api_get()

        if (
            db.private_network is None
            or db.private_network.subnet_id != subnet.id
        ):
            continue

        # This database is not in the process of being detached
        return False

    return True
