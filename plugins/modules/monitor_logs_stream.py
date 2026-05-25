#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for Monitor Logs Streams."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional, Set

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    monitor_logs_stream as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    poll_condition,
    validate_required,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ApiError, LogsStream, LogsStreamDetails

linode_monitor_logs_stream_spec = {
    "id": SpecField(
        type=FieldType.integer,
        required=False,
        description=[
            "The ID of the logs stream. Used to identify an existing stream to update or delete."
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=False,
        editable=True,
        description=[
            "The name of the stream. This is used for display purposes in Akamai Cloud Manager."
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        required=False,
        choices=["audit_logs", "lke_audit_logs"],
        description=[
            "The type of stream. "
            "This can be ``audit_logs`` for logs consisting of all of the control plane "
            "operations for the services in your Linodes, or ``lke_audit_logs`` for log data "
            "for your Linode Kubernetes Engine (LKE) enterprise clusters."
        ],
    ),
    "details": SpecField(
        type=FieldType.dict,
        required=False,
        editable=True,
        description=[
            "Additional details for the stream, based on the selected type.",
            "Currently, this only applies to streams with a type of ``lke_audit_logs``.",
        ],
        suboptions={
            "cluster_ids": SpecField(
                type=FieldType.list,
                element_type=FieldType.integer,
                required=False,
                description=[
                    "The unique identifiers for each LKE enterprise cluster."
                ],
            ),
            "is_auto_add_all_clusters_enabled": SpecField(
                type=FieldType.bool,
                required=False,
                default=False,
                description=[
                    "When set to ``true``, newly added LKE enterprise clusters on your account "
                    "will be included in the stream. "
                    "If ``false``, only existing LKE enterprise clusters are included."
                ],
            ),
        },
    ),
    "status": SpecField(
        type=FieldType.string,
        required=False,
        editable=True,
        choices=["active", "inactive"],
        description=[
            "The availability status of the stream.",
            "While creating or updating, you can pass ``active`` or ``inactive``.",
            "Note that the API might return ``provisioning`` while it is being set up.",
        ],
    ),
    "destinations": SpecField(
        type=FieldType.list,
        element_type=FieldType.integer,
        required=False,
        editable=True,
        description=[
            "List of unique identifiers for the sync points that will receive logs data.",
            "At the moment only a single destination is supported by the API.",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        required=True,
        choices=["present", "absent"],
        description=["The desired state of the logs stream."],
    ),
    "wait": SpecField(
        type=FieldType.bool,
        required=False,
        default=False,
        description=[
            "Wait for the stream to finish provisioning before returning."
        ],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        required=False,
        default=600,
        description=[
            "Time in seconds to wait for the stream to finish provisioning."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Create, update, and delete Monitor Logs Streams.",
        "A stream defines a flow of logs (like audit logs) to a specific destination.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=linode_monitor_logs_stream_spec,
    examples=docs.specdoc_examples,
    return_values={
        "stream": SpecReturnValue(
            type=FieldType.dict,
            description=[
                "A dictionary containing the details of the monitor logs stream."
            ],
            sample=docs.result_stream_samples,
        )
    },
)

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

REQUIRED_PRESENT: Set[str] = {"label", "type", "destinations"}


class LinodeMonitorLogsStream(LinodeModuleBase):
    """Module for creating, updating, and deleting Linode Monitor Logs Streams"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "stream": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
            supports_check_mode=True,
        )

    def _get_stream(
        self, stream_id: Optional[int], label: Optional[str]
    ) -> Any:
        try:
            if stream_id:
                return self.client.load(LogsStream, stream_id)

            if label:
                streams = self.client.monitor.streams(LogsStream.label == label)
                if len(streams) > 0:
                    return streams[0]

            return None
        except ApiError as err:
            if err.status == 404:
                return None
            return self.fail(msg=f"Failed to get monitor logs stream: {err}")

    def _create_stream(self) -> Any:
        params = self.module.params
        label = params.get("label")
        stream_type = params.get("type")
        destinations = params.get("destinations")
        status = params.get("status")
        details = params.get("details")

        details_obj = None
        if details is not None:
            details_obj = LogsStreamDetails(**details)

        self.results["changed"] = True
        self.register_action(f"Created Logs stream {label}")

        if not self.module.check_mode:
            try:
                new_stream = self.client.monitor.stream_create(
                    destinations=destinations,
                    label=label,
                    type=stream_type,
                    status=status,
                    details=details_obj,
                )
                return new_stream
            except Exception as e:
                self.fail(msg=f"Failed to create stream: {e}")

        return None

    def _update_stream(self, stream: Any) -> Any:
        params = self.module.params
        label = params.get("label")
        status = params.get("status")
        destinations = params.get("destinations")
        details = params.get("details")

        needs_save = False
        needs_destination_update = False

        if label and stream.label != label:
            stream.label = label
            needs_save = True
            self.register_action(f"Updated label for stream {stream.id}")

        if status and stream.status != status:
            stream.status = status
            needs_save = True
            self.register_action(f"Updated status for stream {stream.id}")

        if details is not None:
            current_details = getattr(stream, "details", None)
            current_details_dict = (
                current_details.dict if current_details else {}
            )

            merged_details = current_details_dict.copy()
            merged_details.update(details)

            if current_details_dict != merged_details:
                stream.details = LogsStreamDetails(**merged_details)
                needs_save = True
                self.register_action(f"Updated details for stream {stream.id}")

        current_dest_ids = (
            [d.id for d in stream.destinations]
            if getattr(stream, "destinations", None)
            else []
        )
        if destinations is not None and sorted(current_dest_ids) != sorted(
            destinations
        ):
            needs_destination_update = True
            self.register_action(f"Updated destinations for stream {stream.id}")

        if needs_save or needs_destination_update:
            self.results["changed"] = True

            if not self.module.check_mode:
                try:
                    if needs_save:
                        self._wait_for_status(stream, force=True)
                        stream.save()
                    if needs_destination_update:
                        # Destination update requires a separate request due to api asymmetry.
                        # stream.save() can briefly change the status back to provisioning,
                        # so we force wait to avoid race conditions for compound updates
                        self._wait_for_status(stream, force=True)
                        stream.update_destinations(destinations)

                    stream = self.client.load(LogsStream, stream.id)
                except Exception as e:
                    self.fail(msg=f"Failed to update stream: {e}")

        return stream

    def _handle_present(self) -> None:
        params = self.module.params
        stream_id = params.get("id")
        label = params.get("label")

        stream = self._get_stream(stream_id, label)

        if stream is None:
            try:
                validate_required(REQUIRED_PRESENT, params)
            except Exception as exception:
                self.fail(exception)

            stream = self._create_stream()
        else:
            stream = self._update_stream(stream)

        # In check mode during creation, stream will be None, so we return early
        if stream is None and self.module.check_mode:
            self.results["stream"] = {}
            return

        if not self.module.check_mode:
            stream = self._wait_for_status(stream)

        self.results["stream"] = stream._raw_json

    def _handle_absent(self) -> None:
        params = self.module.params
        stream_id = params.get("id")
        label = params.get("label")

        if not stream_id and not label:
            self.fail(
                msg="One of 'id' or 'label' is required for state=absent."
            )

        stream = self._get_stream(stream_id, label)

        if stream is not None:
            self.results["stream"] = stream._raw_json
            self.results["changed"] = True

            self.register_action(f"Deleted logs stream {stream.id}")

            if not self.module.check_mode:
                try:
                    stream.delete()
                except Exception as e:
                    self.fail(msg=f"Failed to delete stream: {e}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Monitor Logs Stream module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()
        return self.results

    def _wait_for_status(self, stream: Any, force: bool = False) -> Any:
        wait = self.module.params.get("wait")
        wait_timeout = self.module.params.get("wait_timeout")

        if not force and not wait:
            return stream

        def _check_status() -> bool:
            current_stream = self.client.load(LogsStream, stream.id)
            return getattr(current_stream, "status", None) in [
                "active",
                "inactive",
            ]

        try:
            poll_condition(_check_status, step=10, timeout=wait_timeout)
            return self.client.load(LogsStream, stream.id)
        except Exception as e:
            return self.fail(
                msg=f"Timeout of {wait_timeout}s exceeded waiting for stream {stream.id} "
                f"to become active or inactive. Error: {e}"
            )


def main() -> None:
    """Constructs and calls the Linode Monitor Logs Stream module"""
    LinodeMonitorLogsStream()


if __name__ == "__main__":
    main()
