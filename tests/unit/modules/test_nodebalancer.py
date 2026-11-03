from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
from ansible_collections.linode.cloud.plugins.modules.nodebalancer import (
    SPECDOC_META,
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


@pytest.mark.parametrize("subnet_id", [None, 12345])
def test_create_node_accepts_optional_subnet_id(subnet_id):
    node_params = {"label": "test-node", "address": "10.0.0.10:80"}
    if subnet_id is not None:
        node_params["subnet_id"] = subnet_id

    validation = ArgumentSpecValidator(SPECDOC_META.ansible_spec).validate(
        {
            "label": "test-nodebalancer",
            "state": "present",
            "configs": [
                {"port": 80, "protocol": "http", "nodes": [node_params]}
            ],
        }
    )
    assert not validation.error_messages

    module = _make_module({})
    config = MagicMock()
    created = object()
    config.node_create.return_value = created

    assert (
        module._create_node(
            config,
            validation.validated_parameters["configs"][0]["nodes"][0],
        )
        is created
    )
    config.node_create.assert_called_once_with(
        "test-node",
        address="10.0.0.10:80",
        subnet_id=subnet_id,
        weight=None,
        mode=None,
    )
