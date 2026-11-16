from copy import copy
from types import SimpleNamespace
from unittest.mock import patch

from ansible_collections.linode.cloud.plugins.module_utils import (
    linode_common_list,
)
from ansible_collections.linode.cloud.plugins.modules import (
    monitor_logs_stream_quota_list,
)


class TestMonitorLogsStreamQuotaList:

    def test_module_configuration(self):
        module = monitor_logs_stream_quota_list.module

        assert module.endpoint_template == "/monitor/streams/quotas"
        assert module.result_field_name == "stream_quotas"
        assert module.disable_filters
        assert set(module.spec.return_values) == {"stream_quotas"}

    def test_returns_quotas_from_sample_api_response(self):
        quotas = [
            {
                "quota_id": "aclp_audit_logs_streams",
                "quota_name": "Number of Audit Logs Streams",
                "description": "Current number of audit logs streams per account",
                "quota_limit": 5,
                "quota_type": "logs_streams_aclp_audit_logs_streams",
            },
            {
                "quota_id": "aclp_lke_audit_logs_streams",
                "quota_name": "Number of LKE Audit Logs Streams",
                "description": "Current number of LKE audit logs streams per account",
                "quota_limit": 10,
                "quota_type": "logs_streams_aclp_lke_audit_logs_streams",
            },
        ]
        module = copy(monitor_logs_stream_quota_list.module)
        module.results = module.results.copy()
        module.module = SimpleNamespace(params={"count": None})
        module._client = object()

        with patch.object(
            linode_common_list, "get_all_paginated", return_value=quotas
        ) as mock_get_all_paginated:
            result = module.exec_module()

        assert result == {"stream_quotas": quotas}
        mock_get_all_paginated.assert_called_once_with(
            module._client,
            "/monitor/streams/quotas",
            None,
            num_results=None,
        )
