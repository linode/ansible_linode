from typing import Any, Optional, List

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_requirements, global_authors
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import filter_null_values, handle_updates

from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import LogsDestination
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.logs_destination as docs
import polling

details_spec: dict = {
    "access_key_id": SpecField(

    ),
}

spec: dict = {
    #fixme REWRITE
    "details": SpecField(
        type=FieldType.dict,
        required=True,
        editable=True,
        suboptions=details_spec,
        description=[
            ""
        ]
    ),
    "wait": SpecField(
        type=FieldType.bool,
        default=False,
        description=["Wait for the logs destination ready"]
    )
}

SPECDOC_META = SpecDocMeta(
    description=[
        "" #fixme
    ],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "logs_destination": SpecReturnValue(
            description="", #fixme
            docs_url="",
            type=FieldType.dict,
            sample=docs.result_logs_destination_sample,
        ),
    },
)


# Fields that can be updated on an existing Logs Destination
MUTABLE_FIELDS = {
    "details",
    "label",
    "type"
}

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


class LinodeLogsDestination(LinodeModuleBase):
    """Module for creating and destroying Logs Destination"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "logs_destination": None,
        }

        self._logs_destination: Optional[LogsDestination] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _wait_for_logs_destination_ready(self, logs_destination: LogsDestination) -> None:
        def poll_func() -> bool:
            logs_destination._api_get()
            return logs_destination.status not in ["inactive"] #fixme?

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
                "failed to wait for logs destination status: timeout period expired"
            )

    def _get_logs_destination(self, destination_id: int
    ) -> Optional[LogsDestination]:
        try:
            return self.client.load(LogsDestination, destination_id)
        except Exception as exception:
            return self.fail(
                msg="failed to get a logs destination id {0}: {1}".format(
                    destination_id, exception
                )
            )

    def _create_logs_destination(self) -> Optional[LogsDestination]:
        params = self.module.params

        try:
            self.register_action(
                "Created logs destination"
            )
            return self.client.monitor.destination_create(
                label=params.pop("label"),
                type=params.pop("type"),
                access_key_id=params.pop("access_key_id"),
                access_key_secret=params.pop("access_key_secret"),
                bucket_name=params.pop("bucket_name"),
                host=params.pop("host"),
                path=params.pop("path"),  # fixme path optional?
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create logs destination: {0}".format(exception)
            )

    def _update_logs_destination(self) -> None:
        """Handles all update functionality for the current Logs Destination"""

        handle_updates(
            self._logs_destination,
            filter_null_values(self.module.params),
            MUTABLE_FIELDS,
            self.register_action,
        )

        if self.module.params.get("wait"):
            self._wait_for_logs_destination_ready(self._logs_destination)

    def _handle_logs_destination(self) -> None:
        params = self.module.params

        destination_id: int = params.get("id")

        if destination_id:
            self._logs_destination = self._get_logs_destination(destination_id)

        # Create logs destination if it does not already exist
        if self.logs_destination is None:
            self._logs_destination = self._create_logs_destination()
            if params.get("wait"):
                self._wait_for_logs_destination_ready(self._logs_destination)

        self._update_logs_destination()

        # Force lazy-loading
        self._logs_destination._api_get()

        self.results["logs_destination"] = self._logs_destination._raw_json

    def _handle_logs_destination_absent(self) -> None:
        destination_id: int = self.module.params.get("id")

        self._logs_destination = self._get_logs_destination(destination_id)

        if self._logs_destination is not None:
            self.results["logs_destination"] = self._logs_destination._raw_json

            self._logs_destination.delete()
            self.register_action(
                "Deleted logs destination {0}".format(destination_id)
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Monitor Logs Destination module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_logs_destination_absent()
            return self.results

        self._handle_logs_destination()
        return self.results


def main() -> None:
    LinodeLogsDestination()


if __name__ == "__main__":
    main()
