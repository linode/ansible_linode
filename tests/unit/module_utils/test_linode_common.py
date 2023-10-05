from types import SimpleNamespace
import os

from ansible_collections.linode.cloud.tests.unit.base import TestModuleBase

class TestLinodeModuleBase():

    def test_module_ca_path_override(self):
        os.environ['LINODE_CA'] = "env_ca"

        mock_module = TestModuleBase()
        mock_module.module = SimpleNamespace(params={
            "api_token":"testing", 
            "api_version": None,
            "api_url":"/", 
            "ua_prefix": None, 
            "ca_path":"foobar"
        })

        client = mock_module.client
        assert client.ca_path == "foobar"