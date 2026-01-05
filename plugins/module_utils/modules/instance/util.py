"""
Contains various helpers relating to the linode.cloud.instance module.
"""

from linode_api4 import Instance

TRANSIENT_STATUSES = {
    "booting": "running",
    "rebooting": "running",
    "shutting_down": "offline",
    "stopped": "offline",
}


def resolve_terminal_status(instance: Instance):
    """
    Returns the terminal status for the given Instance. (e.g. booting -> running)
    """

    return (
        TRANSIENT_STATUSES[instance.status]
        if instance.status in TRANSIENT_STATUSES
        else instance.status
    )
