from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
from ansible_collections.linode.cloud.plugins.modules.nodebalancer_node import (
    SPECDOC_META,
    LinodeNodeBalancerNode,
)


@pytest.mark.parametrize("subnet_id", [None, 12345])
def test_create_node_accepts_optional_subnet_id(subnet_id):
    params = {
        "nodebalancer_id": 123,
        "config_id": 456,
        "label": "test-node",
        "address": "10.0.0.10:80",
        "state": "present",
    }
    if subnet_id is not None:
        params["subnet_id"] = subnet_id

    validation = ArgumentSpecValidator(SPECDOC_META.ansible_spec).validate(
        params
    )
    assert not validation.error_messages

    module = LinodeNodeBalancerNode.__new__(LinodeNodeBalancerNode)
    module.module = SimpleNamespace(params=validation.validated_parameters)
    module._client = MagicMock()
    module.register_action = MagicMock()
    created = SimpleNamespace(id=789)

    with patch(
        "ansible_collections.linode.cloud.plugins.modules.nodebalancer_node.linode_api4.NodeBalancerConfig"
    ) as config_class:
        config_class.return_value.node_create.return_value = created

        assert module._create_node() is created

    config_class.assert_called_once_with(module._client, 456, 123)
    config_class.return_value.node_create.assert_called_once_with(
        "test-node",
        "10.0.0.10:80",
        subnet_id=subnet_id,
        state="present",
        mode=None,
        weight=None,
    )
