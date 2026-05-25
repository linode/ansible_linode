from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from linode_api4 import ApiError

from ansible_collections.linode.cloud.plugins.modules.ip import Module


def _make_module(params: dict) -> Module:
    """
    Constructs a Module instance with a mocked AnsibleModule and LinodeClient.
    """
    base_params = {
        "api_token": "faketoken",
        "api_url": "https://api.linode.com/v4",
        "api_version": None,
        "ua_prefix": None,
        "ca_path": None,
        "linode_id": None,
        "public": None,
        "type": None,
        "address": None,
        "reserved": None,
        "tags": None,
        "state": "present",
    }
    base_params.update(params)

    module_instance = Module.__new__(Module)
    module_instance.module = SimpleNamespace(params=base_params)
    module_instance.results = {
        "changed": False,
        "actions": [],
        "ip": None,
    }
    module_instance._actions = []
    module_instance._client = MagicMock()

    def register_action(msg):
        module_instance.results["actions"].append(msg)
        module_instance.results["changed"] = True

    module_instance.register_action = register_action

    def fail(msg, **kwargs):
        raise Exception(msg)

    module_instance.fail = fail

    return module_instance


class TestIPModuleGetIP:

    def test_get_ip_returns_ip_on_success(self):
        module = _make_module({})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": False}

        with patch(
            "ansible_collections.linode.cloud.plugins.modules.ip.IPAddress",
            return_value=mock_ip,
        ):
            result = module._get_ip("1.2.3.4")

        assert result is mock_ip
        mock_ip._api_get.assert_called_once()

    def test_get_ip_returns_none_on_404(self):
        module = _make_module({})
        mock_ip = MagicMock()
        mock_ip._api_get.side_effect = ApiError("Not found", status=404)

        with patch(
            "ansible_collections.linode.cloud.plugins.modules.ip.IPAddress",
            return_value=mock_ip,
        ):
            result = module._get_ip("1.2.3.4")

        assert result is None

    def test_get_ip_raises_on_non_404_api_error(self):
        module = _make_module({})
        mock_ip = MagicMock()
        mock_ip._api_get.side_effect = ApiError("Server error", status=500)

        with patch(
            "ansible_collections.linode.cloud.plugins.modules.ip.IPAddress",
            return_value=mock_ip,
        ):
            with pytest.raises(Exception, match="failed to get IP address"):
                module._get_ip("1.2.3.4")


class TestIPModuleHandlePresent:

    def test_promote_to_reserved_calls_put(self):
        """When address is given and reserved differs, PUT is called."""
        module = _make_module({"address": "1.2.3.4", "reserved": True})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": False}

        with patch.object(module, "_get_ip", return_value=mock_ip):
            module._handle_present()

        module._client.put.assert_called_once_with(
            "/networking/ips/1.2.3.4",
            data={"reserved": True},
        )
        mock_ip._api_get.assert_called_once()
        assert module.results["ip"] == mock_ip._raw_json
        assert module.results["changed"] is True

    def test_promote_to_reserved_no_op_when_already_reserved(self):
        """When address is given and reserved already matches, PUT is NOT called."""
        module = _make_module({"address": "1.2.3.4", "reserved": True})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": True}

        with patch.object(module, "_get_ip", return_value=mock_ip):
            module._handle_present()

        module._client.put.assert_not_called()
        assert module.results["changed"] is False

    def test_handle_present_fails_when_address_not_found(self):
        """When address is given but IP not found, fail is raised."""
        module = _make_module({"address": "1.2.3.4", "reserved": True})

        with patch.object(module, "_get_ip", return_value=None):
            with pytest.raises(Exception, match="not found"):
                module._handle_present()

    def test_allocate_ip_when_no_address(self):
        """When no address is given, ip_allocate is called."""
        module = _make_module(
            {"linode_id": 123, "public": True, "type": "ipv4"}
        )
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "5.6.7.8", "linode_id": 123}
        module._client.networking.ip_allocate.return_value = mock_ip

        module._handle_present()

        module._client.networking.ip_allocate.assert_called_once_with(123, True)
        assert module.results["ip"] == mock_ip._raw_json
        assert module.results["changed"] is True

    def test_allocate_ip_fails_without_linode_id(self):
        """When no address and no linode_id, fail is raised."""
        module = _make_module({})

        with pytest.raises(Exception, match="linode_id, public, and type are required"):
            module._handle_present()

    def test_promote_to_reserved_put_failure_raises(self):
        """When PUT fails, fail is raised."""
        module = _make_module({"address": "1.2.3.4", "reserved": True})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": False}
        module._client.put.side_effect = Exception("API error")

        with patch.object(module, "_get_ip", return_value=mock_ip):
            with pytest.raises(Exception, match="failed to update IP"):
                module._handle_present()

    def test_update_tags_uses_reserved_ips_endpoint(self):
        """When tags differ, PUT is sent to the reserved-IPs endpoint for idempotency."""
        module = _make_module({"address": "1.2.3.4", "tags": ["test-tag"]})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": True}

        mock_reserved_ip = MagicMock()
        mock_reserved_ip.tags = []  # Current state: no tags

        with patch.object(module, "_get_ip", return_value=mock_ip), patch(
            "ansible_collections.linode.cloud.plugins.modules.ip.ReservedIPAddress",
            return_value=mock_reserved_ip,
        ):
            module._handle_present()

        module._client.put.assert_called_once_with(
            "/networking/reserved/ips/1.2.3.4",
            data={"tags": ["test-tag"]},
        )
        assert module.results["changed"] is True
        assert module.results["ip"]["tags"] == ["test-tag"]

    def test_update_tags_idempotent_when_tags_match(self):
        """When tags already match what the reserved-IPs endpoint returns, no PUT is sent."""
        module = _make_module({"address": "1.2.3.4", "tags": ["test-tag"]})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": True}

        mock_reserved_ip = MagicMock()
        mock_reserved_ip.tags = ["test-tag"]  # Already matches

        with patch.object(module, "_get_ip", return_value=mock_ip), patch(
            "ansible_collections.linode.cloud.plugins.modules.ip.ReservedIPAddress",
            return_value=mock_reserved_ip,
        ):
            module._handle_present()

        module._client.put.assert_not_called()
        assert module.results["changed"] is False
        assert module.results["ip"]["tags"] == ["test-tag"]

    def test_update_tags_fails_when_not_reserved(self):
        """When the reserved-IPs endpoint returns 404, fail with a clear error message."""
        module = _make_module({"address": "1.2.3.4", "tags": ["test-tag"]})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": False}

        mock_reserved_ip = MagicMock()
        mock_reserved_ip._api_get.side_effect = ApiError("Not found", status=404)

        with patch.object(module, "_get_ip", return_value=mock_ip), patch(
            "ansible_collections.linode.cloud.plugins.modules.ip.ReservedIPAddress",
            return_value=mock_reserved_ip,
        ):
            with pytest.raises(
                Exception, match="tags can only be set on reserved IPs"
            ):
                module._handle_present()

    def test_allocate_reserved_ip_includes_public_true(self):
        """POST /networking/ips for a reserved IP must include public=True per the schema."""
        module = _make_module(
            {"region": "us-east", "reserved": True, "type": "ipv4"}
        )
        module._client.post.return_value = {"address": "1.2.3.4", "reserved": True}

        module._handle_present()

        module._client.post.assert_called_once_with(
            "/networking/ips",
            data={
                "type": "ipv4",
                "public": True,
                "region": "us-east",
                "reserved": True,
            },
        )
        assert module.results["ip"] == {"address": "1.2.3.4", "reserved": True}

    def test_no_tags_skips_put_for_tags(self):
        """When tags are not provided, no tags PUT is made."""
        module = _make_module({"address": "1.2.3.4", "reserved": True})
        mock_ip = MagicMock()
        mock_ip._raw_json = {"address": "1.2.3.4", "reserved": True}

        with patch.object(module, "_get_ip", return_value=mock_ip):
            module._handle_present()

        module._client.put.assert_not_called()

    def test_tags_without_address_fails(self):
        """tags requires address; omitting address must raise a clear error."""
        module = _make_module({"tags": ["test-tag"]})

        with pytest.raises(Exception, match="tags requires address to be specified"):
            module._handle_present()

    def test_region_without_reserved_fails(self):
        """region is only valid when reserved=true; omitting reserved must raise a clear error."""
        module = _make_module({"region": "us-east"})

        with pytest.raises(Exception, match="region is only valid when reserved=true"):
            module._handle_present()
