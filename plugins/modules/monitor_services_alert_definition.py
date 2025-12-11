#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module allows users to manage ACLP alert definitions.
"NOTE: This module is under v4beta.","""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.alert_definition as docs
import polling
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import AlertDefinition

dimension_filter_spec: dict = {
    "dimension_label": SpecField(
        type=FieldType.string,
        description=["The name of the dimension to be used in the filter."],
    ),
    "operator": SpecField(
        type=FieldType.string,
        choices=["eq", "neq", "startswith", "endswith"],
        description=[
            "The operator to apply to the dimension filter. "
            "Available values are eq for equal, neq for not equal, startswith, and endswith."
        ],
    ),
    "value": SpecField(
        type=FieldType.string,
        description=["The value to compare the dimension_label against."],
    ),
}

rule_spec: dict = {
    "aggregate_function": SpecField(
        type=FieldType.string,
        choices=["avg", "sum", "min", "max"],
        description=["The aggregation function applied to the metric."],
    ),
    "dimension_filters": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=dimension_filter_spec,
        description=[
            "Individual objects that define dimension filters for the rule."
        ],
    ),
    "metric": SpecField(
        type=FieldType.string, description=["The metric to query."]
    ),
    "operator": SpecField(
        type=FieldType.string,
        choices=["eq", "gt", "lt", "gte", "lte"],
        description=[
            "The operator to apply to the metric. "
            "Available values are eq for equal, "
            "gt for greater than, "
            "lt for less than, "
            "gte for greater than or equal, "
            "and lte for less than or equal."
        ],
    ),
    "threshold": SpecField(
        type=FieldType.float,
        description=[
            "The predefined value or condition that triggers an alert when met or exceeded."
        ],
    ),
}

rule_criteria_spec: dict = {
    "rules": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=rule_spec,
        description=["The individual rules that make up the alert definition."],
    )
}

trigger_conditions_spec: dict = {
    "criteria_condition": SpecField(
        type=FieldType.string,
        choices=["ALL"],
        description=[
            "Signifies the logical operation applied when multiple metrics "
            "are set for an alert definition. "
            "For example, if you wanted to apply both cpu_usage > 90 and memory_usage > 80, "
            "ALL is the criteria_condition. "
            "Currently, only ALL is supported."
        ],
    ),
    "evaluation_period_seconds": SpecField(
        type=FieldType.integer,
        description=[
            "The time period over which data is collected before evaluating "
            "whether the alert definition's threshold has been met or exceeded."
        ],
    ),
    "polling_interval_seconds": SpecField(
        type=FieldType.integer,
        description=[
            "The frequency at which the metric is checked for a change in state. "
            "For example, with cpu_usage set as your metric and this set to 300, "
            "your cpu_usage is checked every 5 minutes for some change in its state."
        ],
    ),
    "trigger_occurrences": SpecField(
        type=FieldType.integer,
        description=[
            "The minimum number of consecutive polling_interval_seconds periods that "
            "the threshold needs to be breached to trigger the alert."
        ],
    ),
}

spec: dict = {
    "service_type": SpecField(
        type=FieldType.string,
        required=True,
        description=["The Akamai Cloud Computing service being monitored."],
    ),
    "channel_ids": SpecField(
        type=FieldType.list,
        required=True,
        editable=True,
        description=[
            "The identifiers for the alert channels to use for the alert. "
            "Run the List alert channels operation and store the id for the applicable channels."
        ],
    ),
    "description": SpecField(
        type=FieldType.string,
        editable=True,
        description=["An additional description for the alert definition."],
    ),
    "entity_ids": SpecField(
        type=FieldType.list,
        editable=True,
        description=[
            "The id for each individual entity from a service_type. "
            "Get this value by running the list operation for the appropriate entity. "
            "For example, if your entity is one of your PostgreSQL databases, "
            "run the List PostgreSQL Managed Databases operation "
            "and store the id for the appropriate database from the response. "
            "You also need read_only access to the scope for the service_type "
            "for each of the entity_ids."
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=True,
        editable=True,
        description=[
            "The name of the alert definition. "
            "This is used for display purposes in Akamai Cloud Manager."
        ],
    ),
    "rule_criteria": SpecField(
        type=FieldType.dict,
        suboptions=rule_criteria_spec,
        required=True,
        editable=True,
        description=["Details for the rules required to trigger the alert."],
    ),
    "severity": SpecField(
        type=FieldType.integer,
        required=True,
        editable=True,
        choices=[0, 1, 2, 3],
        description=[
            "The severity of the alert. "
            "Supported values include 3 for info, "
            "2 for low, 1 for medium, and 0 for severe."
        ],
    ),
    "trigger_conditions": SpecField(
        type=FieldType.dict,
        required=True,
        editable=True,
        suboptions=trigger_conditions_spec,
        description=[
            "The conditions that need to be met to send a notification for the alert."
        ],
    ),
    "id": SpecField(
        type=FieldType.integer,
        description=[
            "The unique identifier assigned to the alert definition. "
            "Run the List alert definitions operation and store the id "
            "for the applicable alert definition. "
            "Required for updating."
        ],
    ),
    "status": SpecField(
        type=FieldType.string,
        editable=True,
        choices=["enabled", "disabled"],
        description=["The current status of the alert."],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "wait": SpecField(
        type=FieldType.bool,
        default=False,
        description=["Wait for the alert definition ready (not in progress)."],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        default=600,
        description=[
            "The amount of time, in seconds, to wait for the alert definition."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage an alert definition for a specific service type. "
        "Akamai refers to these as user alerts. "
        "You need read_only access to the scope for the selected serviceType. "
    ],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "alert_definition": SpecReturnValue(
            description="The alert definition in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-alert-definition",
            type=FieldType.dict,
            sample=docs.result_aclp_alert_definition_sample,
        ),
    },
)

# Fields that can be updated on an existing ACLP alert definition
MUTABLE_FIELDS = {
    "channel_ids",
    "description",
    "entity_ids",
    "label",
    "rule_criteria",
    "severity",
    "status",
    "trigger_conditions",
}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class LinodeMonitorServicesAlertDefinition(LinodeModuleBase):
    """Module for creating and destroying ACLP Monitor Services Alert Definition"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "alert_definition": None,
        }

        self._alert_definition: Optional[AlertDefinition] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _wait_for_alert_definition_ready(
        self, alert_definiton: AlertDefinition
    ) -> None:
        def poll_func() -> bool:
            alert_definiton._api_get()
            return alert_definiton.status not in ["in progress"]

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=10,
                timeout=self._timeout_ctx.seconds_remaining,
            )
        except polling.TimeoutException:
            self.fail(
                "failed to wait for alert definition status: timeout period expired"
            )

    def _get_alert_definition(
        self, alert_id: int, service_type: str
    ) -> Optional[AlertDefinition]:
        try:
            alert_definition = self.client.load(
                AlertDefinition, alert_id, service_type
            )

            return alert_definition
        except Exception as exception:
            return self.fail(
                msg="failed to get an alert definition id {0} service type {1}: {2}".format(
                    alert_id, service_type, exception
                )
            )

    def _create_alert_definition(self) -> Optional[AlertDefinition]:
        params = self.module.params
        service_type = params.pop("service_type")

        try:
            self.register_action(
                "Created alert definition for service type {0}".format(
                    service_type
                )
            )
            return self.client.monitor.create_alert_definition(
                service_type=service_type,
                label=params.pop("label"),
                severity=params.pop("severity"),
                description=params.pop("description"),
                channel_ids=params.pop("channel_ids"),
                rule_criteria=params.pop("rule_criteria"),
                trigger_conditions=params.pop("trigger_conditions"),
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create alert definition: {0}".format(exception)
            )

    def _update_alert_definition(self) -> None:
        """Handles all update functionality for the current Alert Definition"""

        handle_updates(
            self._alert_definition,
            filter_null_values(self.module.params),
            MUTABLE_FIELDS,
            self.register_action,
        )

        if self.module.params.get("wait"):
            self._wait_for_alert_definition_ready(self._alert_definition)

    def _handle_alert_definition(self) -> None:
        params = self.module.params

        service_type: str = params.get("service_type")
        alert_id: int = params.get("id")

        if alert_id:
            self._alert_definition = self._get_alert_definition(
                alert_id, service_type
            )

        # Create the alert definition if it does not already exist
        if self._alert_definition is None:
            self._alert_definition = self._create_alert_definition()
            if params.get("wait"):
                self._wait_for_alert_definition_ready(self._alert_definition)

        self._update_alert_definition()

        # Force lazy-loading
        self._alert_definition._api_get()

        self.results["alert_definition"] = self._alert_definition._raw_json

    def _handle_alert_definition_absent(self) -> None:
        service_type: str = self.module.params.get("service_type")
        alert_id: int = self.module.params.get("id")

        self._alert_definition = self._get_alert_definition(
            alert_id, service_type
        )

        if self._alert_definition is not None:
            self.results["alert_definition"] = self._alert_definition._raw_json

            self._alert_definition.delete()
            self.register_action(
                "Deleted alert definition {0} service type {1}".format(
                    alert_id, service_type
                )
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Monitor Services Alert Definition module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_alert_definition_absent()
            return self.results

        self._handle_alert_definition()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Monitor Services Alert Definition module"""
    LinodeMonitorServicesAlertDefinition()


if __name__ == "__main__":
    main()
