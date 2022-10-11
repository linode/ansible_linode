"""
Shared helper functions and structures for all Managed Database modules.
"""

from typing import Set, Dict, Any, Callable, Optional

from linode_api4 import ApiError

SPEC_UPDATE_WINDOW = dict(
    day_of_week=dict(
        type='int',
        required=True,
        choices=range(1, 8),
        description='The day to perform maintenance. 1=Monday, 2=Tuesday, etc.'
    ),
    duration=dict(
        type='int',
        required=True,
        choices=[1, 3],
        description='The maximum maintenance window time in hours.'
    ),
    frequency=dict(
        type='str',
        choices=['weekly', 'monthly'],
        default='weekly',
        description='Whether maintenance occurs on a weekly or monthly basis.'
    ),
    hour_of_day=dict(
        type='int',
        required=True,
        description='The hour to begin maintenance based in UTC time.',
    ),
    week_of_month=dict(
        type='int',
        description=[
            'The week of the month to perform monthly frequency updates.',
            'Defaults to None.',
            'Required for monthly frequency updates.',
            'Must be null for weekly frequency updates.'
        ]
    )
)

def validate_allow_list(allow_list: Set[str]) -> None:
    """Validates the allow_list field params."""

    for ip_address in allow_list:
        if len(ip_address.split('/')) != 2:
            raise ValueError('Invalid CIDR format for IP {}'.format(ip_address))


def validate_shared_db_input(params: Dict[str, Any]) -> None:
    """Validates the input for shared fields across any Database module."""

    if 'allow_list' in params and params['allow_list'] is not None:
        validate_allow_list(params['allow_list'])


def call_protected_provisioning(func: Callable) -> Optional[Any]:
    """
    Helper function to return None on requests made while a database is provisioning.
    """
    try:
        return func()
    except ApiError as err:
        if err.status == 400:
            # Database is provisioning
            return None

        raise err
