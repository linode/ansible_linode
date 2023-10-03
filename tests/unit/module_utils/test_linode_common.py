from types import SimpleNamespace

from unittest import TestCase
import os

from ansible_collections.linode.cloud.tests.unit.base import TestModuleBase

class TestLinodeModuleBase(TestCase):

    def setUp(self, **kwargs):
        mock_module = TestModuleBase()
        mock_module.module = SimpleNamespace(params=kwargs)

        return mock_module

    def test_module_ca_path_override(self):
        os.environ['LINODE_CA'] = "env_ca"
        mock_module = self.setUp(api_token="testing", api_version=None, api_url="/", ua_prefix=None, ca_path="foobar")

        client = mock_module.client
        assert client.ca_path == "foobar"