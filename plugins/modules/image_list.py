#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode images."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Image",
    result_field_name="images",
    endpoint_template="/images",
    result_docs_url="https://www.linode.com/docs/api/images/#images-list__responses",
    result_samples=docs.result_images_samples,
    examples=docs.specdoc_examples,
)

SPECDOC_META = module.spec

if __name__ == "__main__":
    module.run()
