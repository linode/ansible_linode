from types import SimpleNamespace
import os
from unittest.mock import patch

import pytest
from ansible_collections.linode.cloud.tests.unit.base import TestModuleBase


class TestLinodeModuleBase:

    @pytest.mark.parametrize(
        "api_url",
        ["https://api.linode.com/", "https://api.linode.com"],
    )
    def test_client_api_url_normalization(self, api_url):
        mock_module = TestModuleBase()
        mock_module.module = SimpleNamespace(
            params={
                "api_token": "testing",
                "api_version": "v4",
                "api_url": api_url,
                "ua_prefix": None,
                "ca_path": None,
            }
        )

        with patch(
            "ansible_collections.linode.cloud.plugins.module_utils."
            "linode_common.LinodeClient"
        ) as linode_client:
            mock_module.client

        assert (
            linode_client.call_args.kwargs["base_url"]
            == "https://api.linode.com/v4"
        )

    def test_module_ca_path_override(self):
        os.environ["LINODE_CA"] = "env_ca"

        mock_module = TestModuleBase()
        mock_module.module = SimpleNamespace(
            params={
                "api_token": "testing",
                "api_version": None,
                "api_url": "/",
                "ua_prefix": None,
                "ca_path": "foobar",
            }
        )

        client = mock_module.client
        assert client.ca_path == "foobar"
