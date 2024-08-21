"""Shared documentation objects for use with ansible_specdoc"""

global_authors = [
    "Luke Murphy (@decentral1se)",
    "Charles Kenney (@charliekenney23)",
    "Phillip Campbell (@phillc)",
    "Lena Garber (@lbgarber)",
    "Jacob Riddle (@jriddle)",
    "Zhiwei Liang (@zliang)",
    "Ye Chen (@yechen)",
    "Youjung Kim (@ykim)",
    "Vinay Shanthegowda (@vshanthe)",
    "Erik Zilber (@ezilber)",
]

global_requirements = ["python >= 3"]

BETA_DISCLAIMER = (
    "WARNING! This module makes use of beta endpoints and requires the C(api_version) "
    "field be explicitly set to C(v4beta)."
)
