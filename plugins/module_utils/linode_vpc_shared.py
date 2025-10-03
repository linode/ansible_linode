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

    relevant_dbs = {
        db.id: db
        for db in chain(
            client.database.mysql_instances(),
            client.database.postgresql_instances(),
        )
    }

    # TODO: Use without _raw_json after support added to linode_api4
    subnet._api_get()

    return (
        all(
            subnet_db.id not in relevant_dbs
            or relevant_dbs[subnet_db.id].private_network is None
            or relevant_dbs[subnet_db.id].private_network.subnet_id != subnet.id
            for subnet_db in subnet.databases
        )
        and len(subnet.databases) > 0
    )
