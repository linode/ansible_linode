from typing import Set, Dict, Any


def validate_allow_list(allow_list: Set[str]) -> None:
    for ip_address in allow_list:
        if len(ip_address.split('/')) != 2:
            raise ValueError('Invalid CIDR format for IP {}'.format(ip_address))


def validate_shared_db_input(params: Dict[str, Any]) -> None:
    if 'allow_list' in params and params['allow_list'] is not None:
        validate_allow_list(params['allow_list'])
