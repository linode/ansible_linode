#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Implementation of linode.cloud.database_config_info module.
"""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_config_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import (
    FieldType,
)
from linode_api4 import LinodeClient


def __resolve_by_engine(
    client: LinodeClient, params: Dict[str, Any]
) -> Dict[str, Any]:
    engine_resolvers = {
        "mysql": client.database.mysql_config_options,
        "postgresql": client.database.postgresql_config_options,
    }

    engine = params.get("engine").lower()
    if engine not in engine_resolvers:
        raise ValueError(
            f"Invalid engine {engine}; must be one of {', '.join(engine_resolvers.keys())}."
        )

    return engine_resolvers[engine]()


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="config",
        field_type=FieldType.dict,
        display_name="Configuration",
        docs_url=None,
        samples=docs.result_config_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="Database Engine",
            name="engine",
            type=FieldType.string,
            get=__resolve_by_engine,
        )
    ],
    examples=docs.specdoc_examples,
)

SPECDOC_META = module.spec

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

if __name__ == "__main__":
    module.run()
