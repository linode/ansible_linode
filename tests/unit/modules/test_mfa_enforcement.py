from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import call, patch
from urllib.parse import parse_qs, urlsplit

import pytest
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
from ansible_collections.linode.cloud.plugins.modules import (
    account_settings,
    tfa_optional_user_list,
    tfa_optional_users,
    user_list,
)
from linode_api4 import LinodeClient


def _run_module(module, params, client):
    module._client = client
    module.module = SimpleNamespace(params=params)
    return module.exec_module(**params)


@pytest.mark.parametrize(
    "current,desired,changed",
    [
        (False, True, True),
        (True, False, True),
        (True, True, False),
        (True, None, False),
    ],
)
def test_account_enforcement(current, desired, changed):
    client = LinodeClient("unused-token")
    module = account_settings.Module.__new__(account_settings.Module)
    module.results = {"changed": False, "actions": []}
    settings = {"managed": False, "tfa_enforced": current}
    with (
        patch.object(client, "get", side_effect=lambda *a, **k: dict(settings)),
        patch.object(
            client,
            "put",
            side_effect=lambda *a, data, **k: settings.update(data),
        ) as put,
    ):
        result = _run_module(
            module,
            {"state": "present", "tfa_enforced": desired},
            client,
        )

    assert result["changed"] is changed
    if changed:
        put.assert_called_once()
        assert put.call_args.args == ("/account/settings",)
        assert put.call_args.kwargs["data"] == {"tfa_enforced": desired}
    else:
        put.assert_not_called()
    assert result["account_settings"]["tfa_enforced"] is (
        desired if changed else current
    )


def _user(username):
    return {"username": username, "url": f"/account/users/{username}"}


def test_account_enforcement_rejects_an_older_sdk():
    client = LinodeClient("unused-token")
    module = account_settings.Module.__new__(account_settings.Module)
    with (
        patch.object(account_settings.AccountSettings, "properties", {}),
        patch.object(
            client,
            "get",
            return_value={"managed": False, "tfa_enforced": False},
        ),
        patch.object(client, "put") as put,
        pytest.raises(RuntimeError, match="SDK with MFA enforcement support"),
    ):
        _run_module(module, {"state": "present", "tfa_enforced": True}, client)
    put.assert_not_called()


@pytest.mark.parametrize(
    "desired,changed",
    [
        (["second", "first"], False),
        (["third"], True),
        ([], True),
    ],
)
def test_reconcile_exemptions(desired, changed):
    client = LinodeClient("unused-token")
    module = tfa_optional_users.Module.__new__(tfa_optional_users.Module)
    module.results = {"changed": False, "actions": []}
    original = ["first", "second"]
    stored = original.copy()

    def get(endpoint, **kwargs):
        assert endpoint.startswith("/account/tfa-optional-users")
        # One record per page so comparison must include all pages.
        page = int(parse_qs(urlsplit(endpoint).query).get("page", ["1"])[0])
        return {
            "page": page,
            "pages": max(1, len(stored)),
            "results": len(stored),
            "data": [_user(name) for name in stored[page - 1 : page]],
        }

    def put(endpoint, data):
        stored[:] = data["usernames"]
        return {"tfa_optional_users_count": len(stored), "url": endpoint}

    with (
        patch.object(client, "get", side_effect=get),
        patch.object(client, "put", side_effect=put) as mock_put,
    ):
        result = _run_module(module, {"usernames": desired}, client)

    assert result["changed"] is changed
    if changed:
        mock_put.assert_called_once_with(
            "/account/tfa-optional-users", data={"usernames": desired}
        )
        assert result["tfa_optional_users"] == [_user(name) for name in desired]
    else:
        mock_put.assert_not_called()
        assert result["tfa_optional_users"] == [
            _user(name) for name in original
        ]


def test_list_exemptions_paginates_and_limits_results():
    module = deepcopy(tfa_optional_user_list.module)
    client = LinodeClient("unused-token")
    with patch.object(
        client,
        "get",
        side_effect=[
            {"page": 1, "pages": 3, "data": [_user("first")]},
            {"page": 2, "pages": 3, "data": [_user("second"), _user("third")]},
        ],
    ) as get:
        result = _run_module(module, {"count": 2}, client)

    assert result["tfa_optional_users"] == [_user("first"), _user("second")]
    assert get.call_args_list == [
        call(
            f"/account/tfa-optional-users?page={page}&page_size=25",
            filters=None,
        )
        for page in [1, 2]
    ]


def test_user_list_passes_boolean_enforcement_filters():
    module = deepcopy(user_list.module)
    validated = ArgumentSpecValidator(module.module_arg_spec).validate(
        {
            "filters": [
                {"name": "tfa_enforced", "values": [True, "false"]},
                {"name": "username", "values": ["false"]},
            ],
        }
    )
    assert not validated.error_messages
    client = LinodeClient("unused-token")
    users = [{"username": "false", "tfa_enforced": True}]
    with patch.object(
        client, "get", return_value={"page": 1, "pages": 1, "data": users}
    ) as get:
        result = _run_module(module, validated.validated_parameters, client)

    assert result["users"] == users
    get.assert_called_once_with(
        "/account/users?page=1&page_size=100",
        filters={
            "+and": [
                {"+or": [{"tfa_enforced": True}, {"tfa_enforced": False}]},
                {"+or": [{"username": "false"}]},
            ],
            "+order": "asc",
        },
    )
