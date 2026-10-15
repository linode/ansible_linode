from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from ansible_collections.linode.cloud.plugins.modules.nodebalancer import (
    LinodeNodeBalancer,
)


def _make_module(params: dict) -> LinodeNodeBalancer:
    module = LinodeNodeBalancer.__new__(LinodeNodeBalancer)
    module_params = {
        "label": "test-nodebalancer",
        "region": "us-east",
        "client_conn_throttle": None,
        "client_udp_sess_throttle": None,
        "firewall_id": None,
        "tags": None,
        "ipv4": None,
        "type": None,
        "backend_connectivity": None,
        "vpcs": None,
    }
    module_params.update(params)
    module.module = SimpleNamespace(params=module_params)
    module._client = MagicMock()
    module.register_action = MagicMock()
    return module


def test_create_nodebalancer_passes_connectivity_options():
    module = _make_module(
        {
            "type": "premium",
            "backend_connectivity": "vpc",
            "vpcs": [{"subnet_id": 12345, "ipv4_range": "10.0.0.0/24"}],
        }
    )
    created = object()
    module._client.nodebalancer_create.return_value = created

    assert module._create_nodebalancer() is created
    module._client.nodebalancer_create.assert_called_once_with(
        "us-east",
        label="test-nodebalancer",
        type="premium",
        backend_connectivity="vpc",
        vpcs=[{"subnet_id": 12345, "ipv4_range": "10.0.0.0/24"}],
    )


def test_update_nodebalancer_ignores_creation_only_options():
    module = _make_module(
        {
            "type": "premium",
            "backend_connectivity": "ipv6",
            "vpcs": [{"subnet_id": 12345}],
        }
    )
    module._node_balancer = MagicMock()

    with patch(
        "ansible_collections.linode.cloud.plugins.modules.nodebalancer.handle_updates"
    ) as handle_updates:
        module._update_nodebalancer()

    update_params = handle_updates.call_args.args[1]
    assert "type" not in update_params
    assert "backend_connectivity" not in update_params
    assert "vpcs" not in update_params
