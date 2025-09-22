import ipaddress
from typing import Optional, Tuple


def auto_alloc_ranges_equivalent(
    range1: str,
    range2: str,
) -> bool:
    """
    Returns whether the given ranges auto-alloc ranges are semantically equivalent.
    These ranges accept an explicit range, a prefix, or "auto".
    """

    def __parse_range_components(r: str) -> Tuple[Optional[str], int]:
        segments = r.split("/")
        if len(segments) != 2:
            raise ValueError(f"{r} is not a valid IPv6 range")

        return segments[0] if len(segments[0]) > 0 else None, int(segments[1])

    if "auto" in (range1, range2):
        return True

    r1_address, r1_prefix = __parse_range_components(range1)
    r2_address, r2_prefix = __parse_range_components(range2)

    if r1_address is None or r2_address is None:
        return r1_prefix == r2_prefix

    return (
        ipaddress.ip_address(r1_address) == ipaddress.ip_address(r2_address)
        and r1_prefix == r2_prefix
    )
