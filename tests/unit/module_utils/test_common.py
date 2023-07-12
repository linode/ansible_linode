from types import SimpleNamespace

import pytest

from unittest.mock import patch
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase


@pytest.fixture
def test_module_base():
    return LinodeModuleBase.__new__(LinodeModuleBase)


class TestModuleBase:
    def test_dep_out_of_date(self, test_module_base):
        def fail_handler(msg=None):
            assert "Python package test-dep is out of date " \
                   "(Got test-dep==5.5.4; expected test_dep>=5.5.5). " \
                   "To install the latest dependencies, run " \
                   "`pip install --upgrade -r " \
                   "https://raw.githubusercontent.com/linode/" \
                   "ansible_linode/main/requirements.txt`" in msg

        test_module_base.fail = fail_handler
        with patch(
                "ansible_collections.linode.cloud.plugins.module_utils.linode_common.REQUIREMENTS",
                """test_dep>=5.5.5"""
        ), patch("pkg_resources.require", lambda pkg: [SimpleNamespace(version="5.5.4")]):
            test_module_base._validate_dependencies()

    def test_dep_missing(self, test_module_base):
        def fail_handler(msg=None):
            assert "Python package fake-dep is out of date " \
                   "(Got fake-dep==5.5.4; expected fake_dep>=5.5.5). " \
                   "To install the latest dependencies, run " \
                   "`pip install --upgrade -r https://raw.githubusercontent.com" \
                   "/linode/ansible_linode/main/requirements.txt`" in msg

        test_module_base.fail = fail_handler
        with patch(
                "ansible_collections.linode.cloud.plugins.module_utils.linode_common.REQUIREMENTS",
                """fake_dep>=5.5.5"""
        ), patch("pkg_resources.require", lambda pkg: [SimpleNamespace(version="5.5.4")]):
            test_module_base._validate_dependencies()

    def test_dep_valid(self, test_module_base):
        with patch(
                "ansible_collections.linode.cloud.plugins.module_utils.linode_common.REQUIREMENTS",
                """test_dep>=5.5.5"""
        ), patch("pkg_resources.require", lambda pkg: [SimpleNamespace(version="5.5.5")]):
            test_module_base._validate_dependencies()
