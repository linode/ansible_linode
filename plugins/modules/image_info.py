#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode image."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Image

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Image",
        field_name="image",
        field_type=FieldType.dict,
        docs_url="https://www.linode.com/docs/api/images/#image-view__responses",
        samples=docs_parent.result_image_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                Image, params.get("id")
            )._raw_json,
        ),
        InfoModuleAttr(
            name="label",
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.images,
                Image.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
    ],
)

<<<<<<< HEAD
SPECDOC_META = module.spec
=======
DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"image": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
            mutually_exclusive=[("id", "label")],
        )

    def _get_image_by_label(self, label: str) -> Optional[Image]:
        try:
            return self.client.images(Image.label == label)[0]
        except IndexError:
            return self.fail(
                msg="failed to get image with label {0}: "
                "image does not exist".format(label)
            )
        except Exception as exception:
            return self.fail(
                msg="failed to get image {0}: {1}".format(label, exception)
            )

    def _get_image_by_id(self, image_id: int) -> Image:
        return self._get_resource_by_id(Image, image_id)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for user info module"""

        params = filter_null_values(self.module.params)

        if "id" in params:
            self.results["image"] = self._get_image_by_id(
                params.get("id")
            )._raw_json

        if "label" in params:
            self.results["image"] = self._get_image_by_label(
                params.get("label")
            )._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()

>>>>>>> dev

if __name__ == "__main__":
    module.run()
