from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from ansible_collections.linode.cloud.plugins.modules.iam_role_permissions import (
    Module,
    normalize_account_access,
    normalize_entity_access,
)

CURRENT = {
    "account_access": ["account_linode_admin", "firewall_creator"],
    "entity_access": [
        {"id": 1, "type": "linode", "roles": ["linode_contributor"]},
        {"id": 2, "type": "firewall", "roles": ["firewall_admin"]},
    ],
}


def _make_module(params: dict, check_mode: bool = False) -> Module:
    base_params = {
        "username": "my-user",
        "account_access": None,
        "entity_access": None,
        "state": "present",
    }
    base_params.update(params)

    module_instance = Module.__new__(Module)
    module_instance.module = SimpleNamespace(
        params=base_params, check_mode=check_mode
    )
    module_instance.results = {
        "changed": False,
        "actions": [],
        "role_permissions": None,
    }
    module_instance._client = MagicMock()
    module_instance._client.iam.role_permissions_user_get.return_value = CURRENT
    module_instance._client.iam.role_permissions_user_set.side_effect = (
        lambda username, account_access, entity_access: {
            "account_access": account_access,
            "entity_access": entity_access,
        }
    )

    def fail(msg, **kwargs):
        raise Exception(msg)

    module_instance.fail = fail

    return module_instance


class TestNormalize:
    def test_account_access_ignores_order_and_duplicates(self):
        assert normalize_account_access(["b", "a", "b"]) == ["a", "b"]
        assert normalize_account_access(None) == []

    def test_entity_access_ignores_order(self):
        reordered = list(reversed(CURRENT["entity_access"]))

        assert normalize_entity_access(reordered) == normalize_entity_access(
            CURRENT["entity_access"]
        )


class TestUpdate:
    def test_no_change_when_roles_match(self):
        module = _make_module(
            {
                "account_access": list(reversed(CURRENT["account_access"])),
                "entity_access": list(reversed(CURRENT["entity_access"])),
            }
        )

        module._update()

        assert not module.results["changed"]
        module.client.iam.role_permissions_user_set.assert_not_called()
        assert module.results["role_permissions"] == CURRENT

    def test_account_access_change_preserves_entity_access(self):
        module = _make_module({"account_access": ["account_admin"]})

        module._update()

        assert module.results["changed"]
        module.client.iam.role_permissions_user_set.assert_called_once_with(
            "my-user",
            account_access=["account_admin"],
            entity_access=CURRENT["entity_access"],
        )
        assert module.results["role_permissions"]["account_access"] == [
            "account_admin"
        ]

    def test_entity_access_change_preserves_account_access(self):
        new_entity_access = [
            {"id": 1, "type": "linode", "roles": ["linode_admin"]}
        ]
        module = _make_module({"entity_access": new_entity_access})

        module._update()

        assert module.results["changed"]
        module.client.iam.role_permissions_user_set.assert_called_once_with(
            "my-user",
            account_access=CURRENT["account_access"],
            entity_access=new_entity_access,
        )

    def test_empty_entity_access_clears_roles(self):
        module = _make_module({"entity_access": []})

        module._update()

        assert module.results["changed"]
        module.client.iam.role_permissions_user_set.assert_called_once_with(
            "my-user",
            account_access=CURRENT["account_access"],
            entity_access=[],
        )

    def test_check_mode_does_not_update(self):
        module = _make_module(
            {"account_access": ["account_admin"]}, check_mode=True
        )

        module._update()

        assert module.results["changed"]
        module.client.iam.role_permissions_user_set.assert_not_called()

    def test_get_failure_fails(self):
        module = _make_module({})
        module.client.iam.role_permissions_user_get.side_effect = Exception(
            "boom"
        )

        with pytest.raises(Exception, match="failed to get role permissions"):
            module._update()
