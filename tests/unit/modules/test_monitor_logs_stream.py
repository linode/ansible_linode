from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
from ansible_collections.linode.cloud.plugins.modules.monitor_logs_stream import (
    SPECDOC_META,
    LinodeMonitorLogsStream,
)
from linode_api4 import (
    LogsStream,
    LogsStreamDetails,
    VpnGatewayLogsStreamDetails,
)


class ModuleFailure(Exception):
    pass


def _fail_json(*, msg, **kwargs):
    raise ModuleFailure(msg)


def _make_module(params=None, check_mode=False):
    base_params = {
        "id": None,
        "label": None,
        "type": None,
        "details": None,
        "status": None,
        "destinations": None,
        "state": "present",
        "wait": False,
        "wait_timeout": 600,
    }
    base_params.update(params or {})

    module = LinodeMonitorLogsStream.__new__(LinodeMonitorLogsStream)
    module.module = SimpleNamespace(
        params=base_params,
        check_mode=check_mode,
        fail_json=MagicMock(side_effect=_fail_json),
    )
    module.results = {"changed": False, "actions": [], "stream": None}
    module._client = MagicMock()
    module._wait_for_status = MagicMock(
        side_effect=lambda stream, **kwargs: stream
    )
    return module


def _make_stream(stream_type, details):
    stream = MagicMock()
    stream.id = 9876
    stream.label = "existing-stream"
    stream.type = stream_type
    stream.status = "active"
    stream.details = details
    stream.destinations = [SimpleNamespace(id=12345)]
    stream._raw_json = {"id": 9876, "type": stream_type}
    return stream


@pytest.fixture(params=["vpngw_ipsec_logs", "vpngw_bgp_logs"])
def vpn_type(request):
    return request.param


@pytest.fixture
def vpn_stream(vpn_type):
    return _make_stream(
        vpn_type, VpnGatewayLogsStreamDetails(vpn_gateway_ids=[50, 60])
    )


INVALID_VPN_DETAILS = [
    pytest.param(None, "non-empty list", id="missing-details"),
    pytest.param({}, "non-empty list", id="missing-ids"),
    pytest.param({"vpn_gateway_ids": None}, "non-empty list", id="null-ids"),
    pytest.param({"vpn_gateway_ids": []}, "non-empty list", id="empty-ids"),
    pytest.param({"vpn_gateway_ids": "50"}, "non-empty list", id="not-a-list"),
    pytest.param(
        {"vpn_gateway_ids": [50, 50]}, "unique IDs", id="duplicate-ids"
    ),
    pytest.param({"vpn_gateway_ids": [0]}, "positive integers", id="zero-id"),
    pytest.param(
        {"vpn_gateway_ids": [-1]}, "positive integers", id="negative-id"
    ),
    pytest.param(
        {"vpn_gateway_ids": [True]}, "positive integers", id="true-id"
    ),
    pytest.param(
        {"vpn_gateway_ids": [False]}, "positive integers", id="false-id"
    ),
    pytest.param(
        {"vpn_gateway_ids": [50.5]}, "positive integers", id="float-id"
    ),
    pytest.param(
        {"vpn_gateway_ids": ["50"]}, "positive integers", id="string-id"
    ),
    pytest.param(
        {"vpn_gateway_ids": [None]}, "positive integers", id="null-id"
    ),
    pytest.param(
        {"vpn_gateway_ids": [50, 60], "cluster_ids": []},
        "cluster_ids is not allowed",
        id="empty-lke-clusters",
    ),
    pytest.param(
        {"vpn_gateway_ids": [50, 60], "cluster_ids": [10]},
        "cluster_ids is not allowed",
        id="lke-clusters",
    ),
    pytest.param(
        {
            "vpn_gateway_ids": [50, 60],
            "is_auto_add_all_clusters_enabled": False,
        },
        "is_auto_add_all_clusters_enabled is not allowed",
        id="lke-auto-add-false",
    ),
    pytest.param(
        {
            "vpn_gateway_ids": [50, 60],
            "is_auto_add_all_clusters_enabled": True,
        },
        "is_auto_add_all_clusters_enabled is not allowed",
        id="lke-auto-add-true",
    ),
]


def test_argument_spec_accepts_vpn_without_lke_defaults(vpn_type):
    result = ArgumentSpecValidator(SPECDOC_META.ansible_spec).validate(
        {
            "type": vpn_type,
            "details": {"vpn_gateway_ids": [50, 60]},
            "state": "present",
        }
    )

    assert result.error_messages == []
    details = result.validated_parameters["details"]
    assert details["vpn_gateway_ids"] == [50, 60]
    assert details["cluster_ids"] is None
    assert details["is_auto_add_all_clusters_enabled"] is None


def test_argument_spec_preserves_explicit_false(vpn_type):
    result = ArgumentSpecValidator(SPECDOC_META.ansible_spec).validate(
        {
            "type": vpn_type,
            "details": {
                "vpn_gateway_ids": [50],
                "is_auto_add_all_clusters_enabled": False,
            },
            "state": "present",
        }
    )

    assert result.error_messages == []
    module = _make_module()
    with pytest.raises(ModuleFailure, match="is not allowed"):
        module._build_vpn_stream_details(result.validated_parameters["details"])


@pytest.mark.parametrize("ids", [[1], [50, 60], [60, 50]])
def test_build_vpn_details_contains_only_gateway_ids(ids):
    module = _make_module()
    details = {
        "vpn_gateway_ids": ids,
        "cluster_ids": None,
        "is_auto_add_all_clusters_enabled": None,
    }
    original = deepcopy(details)

    result = module._build_vpn_stream_details(details)

    assert isinstance(result, VpnGatewayLogsStreamDetails)
    assert result.dict == {"vpn_gateway_ids": ids}
    assert details == original
    assert module._client.mock_calls == []


@pytest.mark.parametrize("check_mode", [False, True])
def test_create_vpn_stream(vpn_type, check_mode):
    module = _make_module(
        {
            "label": "vpn-logs",
            "type": vpn_type,
            "status": "active",
            "destinations": [12345],
            "details": {
                "vpn_gateway_ids": [50, 60],
                "cluster_ids": None,
                "is_auto_add_all_clusters_enabled": None,
            },
        },
        check_mode=check_mode,
    )

    result = module._create_stream()

    assert module.results["changed"] is True
    assert module.results["actions"]
    if check_mode:
        assert result is None
        assert module._client.mock_calls == []
    else:
        create = module._client.monitor.stream_create
        create.assert_called_once_with(
            destinations=[12345],
            label="vpn-logs",
            type=vpn_type,
            status="active",
            details=VpnGatewayLogsStreamDetails(vpn_gateway_ids=[50, 60]),
        )
        assert result is create.return_value
        assert create.call_args.kwargs["details"].dict == {
            "vpn_gateway_ids": [50, 60]
        }


@pytest.mark.parametrize("check_mode", [False, True])
@pytest.mark.parametrize("details,error", INVALID_VPN_DETAILS)
def test_create_vpn_rejects_invalid_details(
    vpn_type, check_mode, details, error
):
    module = _make_module(
        {"type": vpn_type, "details": deepcopy(details)},
        check_mode=check_mode,
    )

    with pytest.raises(ModuleFailure, match=error):
        module._create_stream()

    assert module.results["changed"] is False
    assert module.results["actions"] == []
    assert module._client.mock_calls == []


@pytest.mark.parametrize("check_mode", [False, True])
def test_update_vpn_replaces_gateway_ids(vpn_stream, check_mode):
    supplied_details = {
        "vpn_gateway_ids": [70],
        "cluster_ids": None,
        "is_auto_add_all_clusters_enabled": None,
    }
    module = _make_module({"details": supplied_details}, check_mode=check_mode)
    module._client.load.return_value = vpn_stream
    original_details = vpn_stream.details

    result = module._update_stream(vpn_stream)

    assert result is vpn_stream
    assert module.results["changed"] is True
    assert isinstance(vpn_stream.details, VpnGatewayLogsStreamDetails)
    assert vpn_stream.details.dict == {"vpn_gateway_ids": [70]}
    assert original_details.dict == {"vpn_gateway_ids": [50, 60]}
    assert supplied_details["vpn_gateway_ids"] == [70]
    if check_mode:
        vpn_stream.save.assert_not_called()
        module._wait_for_status.assert_not_called()
        assert module._client.mock_calls == []
    else:
        vpn_stream.save.assert_called_once_with()
        module._wait_for_status.assert_called_once_with(vpn_stream, force=True)
        module._client.load.assert_called_once_with(LogsStream, 9876)
    vpn_stream.update_destinations.assert_not_called()


@pytest.mark.parametrize("check_mode", [False, True])
@pytest.mark.parametrize(
    "details",
    [
        None,
        {},
        {"vpn_gateway_ids": None},
        {"vpn_gateway_ids": [50, 60]},
        {
            "vpn_gateway_ids": [60, 50],
            "cluster_ids": None,
            "is_auto_add_all_clusters_enabled": None,
        },
    ],
)
def test_update_vpn_is_idempotent(vpn_stream, check_mode, details):
    module = _make_module({"details": deepcopy(details)}, check_mode=check_mode)
    original_details = vpn_stream.details

    assert module._update_stream(vpn_stream) is vpn_stream

    assert module.results["changed"] is False
    assert module.results["actions"] == []
    assert vpn_stream.details is original_details
    vpn_stream.save.assert_not_called()
    vpn_stream.update_destinations.assert_not_called()
    module._wait_for_status.assert_not_called()
    assert module._client.mock_calls == []


@pytest.mark.parametrize("check_mode", [False, True])
@pytest.mark.parametrize(
    "details,error",
    [
        case
        for case in INVALID_VPN_DETAILS
        if case.id not in {"missing-details", "missing-ids", "null-ids"}
    ],
)
def test_update_vpn_rejects_invalid_details(
    vpn_stream, check_mode, details, error
):
    module = _make_module({"details": deepcopy(details)}, check_mode=check_mode)
    original_details = vpn_stream.details

    with pytest.raises(ModuleFailure, match=error):
        module._update_stream(vpn_stream)

    assert module.results["changed"] is False
    assert module.results["actions"] == []
    assert vpn_stream.details is original_details
    vpn_stream.save.assert_not_called()
    vpn_stream.update_destinations.assert_not_called()
    assert module._client.mock_calls == []


@pytest.mark.parametrize("check_mode", [False, True])
@pytest.mark.parametrize(
    "params,attribute,value",
    [
        ({"label": "renamed"}, "label", "renamed"),
        ({"status": "inactive"}, "status", "inactive"),
    ],
)
def test_update_vpn_without_details(
    vpn_stream, check_mode, params, attribute, value
):
    module = _make_module(params, check_mode=check_mode)
    module._client.load.return_value = vpn_stream
    original_details = vpn_stream.details

    module._update_stream(vpn_stream)

    assert getattr(vpn_stream, attribute) == value
    assert vpn_stream.details is original_details
    assert module.results["changed"] is True
    assert vpn_stream.save.call_count == (0 if check_mode else 1)
    if check_mode:
        assert module._client.mock_calls == []


@pytest.mark.parametrize("check_mode", [False, True])
def test_update_vpn_destinations_without_details(vpn_stream, check_mode):
    module = _make_module({"destinations": [54321]}, check_mode=check_mode)
    module._client.load.return_value = vpn_stream
    original_details = vpn_stream.details

    module._update_stream(vpn_stream)

    assert module.results["changed"] is True
    assert vpn_stream.details is original_details
    vpn_stream.save.assert_not_called()
    if check_mode:
        vpn_stream.update_destinations.assert_not_called()
        assert module._client.mock_calls == []
    else:
        vpn_stream.update_destinations.assert_called_once_with([54321])


@pytest.mark.parametrize("check_mode", [False, True])
def test_update_vpn_details_and_destinations(vpn_stream, check_mode):
    module = _make_module(
        {
            "details": {"vpn_gateway_ids": [70]},
            "destinations": [54321],
        },
        check_mode=check_mode,
    )
    module._client.load.return_value = vpn_stream

    module._update_stream(vpn_stream)

    assert module.results["changed"] is True
    assert vpn_stream.details.dict == {"vpn_gateway_ids": [70]}
    if check_mode:
        vpn_stream.save.assert_not_called()
        vpn_stream.update_destinations.assert_not_called()
        assert module._client.mock_calls == []
    else:
        vpn_stream.save.assert_called_once_with()
        vpn_stream.update_destinations.assert_called_once_with([54321])
        assert module._wait_for_status.call_count == 2
        module._client.load.assert_called_once_with(LogsStream, 9876)


def test_create_vpn_surfaces_sdk_error(vpn_type):
    module = _make_module(
        {
            "type": vpn_type,
            "details": {"vpn_gateway_ids": [50]},
        }
    )
    module._client.monitor.stream_create.side_effect = RuntimeError(
        "SDK failure"
    )

    with pytest.raises(
        ModuleFailure, match="Failed to create stream: SDK failure"
    ):
        module._create_stream()


def test_update_vpn_surfaces_sdk_error(vpn_stream):
    module = _make_module({"details": {"vpn_gateway_ids": [70]}})
    vpn_stream.save.side_effect = RuntimeError("SDK failure")

    with pytest.raises(
        ModuleFailure, match="Failed to update stream: SDK failure"
    ):
        module._update_stream(vpn_stream)

    module._client.load.assert_not_called()


@pytest.mark.parametrize("check_mode", [False, True])
def test_lke_create_preserves_default_false(check_mode):
    module = _make_module(
        {
            "type": "lke_audit_logs",
            "details": {
                "cluster_ids": [10],
                "vpn_gateway_ids": None,
                "is_auto_add_all_clusters_enabled": None,
            },
        },
        check_mode=check_mode,
    )

    module._create_stream()

    assert module.results["changed"] is True
    if check_mode:
        assert module._client.mock_calls == []
    else:
        details = module._client.monitor.stream_create.call_args.kwargs[
            "details"
        ]
        assert isinstance(details, LogsStreamDetails)
        assert details.dict == {
            "cluster_ids": [10],
            "is_auto_add_all_clusters_enabled": False,
        }


def test_lke_create_preserves_explicit_true():
    module = _make_module(
        {
            "type": "lke_audit_logs",
            "details": {
                "cluster_ids": None,
                "vpn_gateway_ids": None,
                "is_auto_add_all_clusters_enabled": True,
            },
        }
    )

    module._create_stream()

    details = module._client.monitor.stream_create.call_args.kwargs["details"]
    assert isinstance(details, LogsStreamDetails)
    assert details.is_auto_add_all_clusters_enabled is True


@pytest.mark.parametrize("check_mode", [False, True])
@pytest.mark.parametrize(
    "details,changed",
    [
        (None, False),
        ({"cluster_ids": [10], "vpn_gateway_ids": None}, False),
        ({"cluster_ids": [20], "vpn_gateway_ids": None}, True),
    ],
)
def test_lke_update_preserves_existing_behavior(check_mode, details, changed):
    stream = _make_stream("lke_audit_logs", LogsStreamDetails(cluster_ids=[10]))
    module = _make_module({"details": deepcopy(details)}, check_mode=check_mode)
    module._client.load.return_value = stream

    module._update_stream(stream)

    assert module.results["changed"] is changed
    assert isinstance(stream.details, LogsStreamDetails)
    assert stream.details.is_auto_add_all_clusters_enabled is False
    assert stream.details.cluster_ids == ([20] if changed else [10])
    assert stream.save.call_count == int(changed and not check_mode)
    if check_mode or not changed:
        assert module._client.mock_calls == []


def test_lke_update_preserves_explicit_true():
    stream = _make_stream("lke_audit_logs", LogsStreamDetails(cluster_ids=[10]))
    module = _make_module(
        {"details": {"is_auto_add_all_clusters_enabled": True}}
    )
    module._client.load.return_value = stream

    module._update_stream(stream)

    assert stream.details.cluster_ids == [10]
    assert stream.details.is_auto_add_all_clusters_enabled is True
    stream.save.assert_called_once_with()


@pytest.mark.parametrize("stream_type", ["audit_logs", "lke_audit_logs"])
@pytest.mark.parametrize("check_mode", [False, True])
@pytest.mark.parametrize("operation", ["create", "update"])
def test_non_vpn_rejects_gateway_ids(stream_type, check_mode, operation):
    module = _make_module(
        {
            "type": stream_type,
            "details": {"vpn_gateway_ids": [50]},
        },
        check_mode=check_mode,
    )
    stream = _make_stream(stream_type, LogsStreamDetails())

    with pytest.raises(ModuleFailure, match="only allowed for VPN"):
        if operation == "create":
            module._create_stream()
        else:
            module._update_stream(stream)

    assert module.results["changed"] is False
    assert module._client.mock_calls == []
    stream.save.assert_not_called()


def test_audit_create_without_details():
    module = _make_module({"type": "audit_logs"})

    module._create_stream()

    assert (
        module._client.monitor.stream_create.call_args.kwargs["details"] is None
    )


def test_handle_present_vpn_create_in_check_mode(vpn_type):
    module = _make_module(
        {
            "type": vpn_type,
            "label": "vpn-logs",
            "destinations": [12345],
            "details": {"vpn_gateway_ids": [50]},
        },
        check_mode=True,
    )
    module._get_stream = MagicMock(return_value=None)

    module._handle_present()

    assert module.results["changed"] is True
    assert module.results["stream"] == {}
    assert module._client.mock_calls == []


def test_handle_present_updates_vpn_by_id(vpn_stream):
    module = _make_module({"id": 9876, "details": {"vpn_gateway_ids": [70]}})
    module._client.load.return_value = vpn_stream

    module._handle_present()

    assert module.module.params["type"] is None
    assert module.results["changed"] is True
    assert module.results["stream"] == vpn_stream._raw_json
    assert vpn_stream.details.dict == {"vpn_gateway_ids": [70]}
    vpn_stream.save.assert_called_once_with()


@pytest.mark.parametrize("check_mode", [False, True])
def test_delete_vpn_without_details(vpn_stream, check_mode):
    module = _make_module(
        {"id": 9876, "state": "absent"}, check_mode=check_mode
    )
    module._client.load.return_value = vpn_stream

    result = module.exec_module(state="absent")

    assert result["changed"] is True
    assert result["stream"] == vpn_stream._raw_json
    assert vpn_stream.delete.call_count == (0 if check_mode else 1)
