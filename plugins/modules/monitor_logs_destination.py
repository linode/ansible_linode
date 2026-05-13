#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module allows users to manage ACLP logs destinations."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.logs_destination as docs
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
from linode_api4 import (
    AkamaiObjectStorageLogsDestinationDetails,
    BasicAuthenticationDetails,
    ClientCertificateDetails,
    CustomHeader,
    CustomHTTPSLogsDestinationDetails,
    DestinationAuthentication,
    LogsDestination,
)

authentication_details_spec: dict = {
    "basic_authentication_password": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The password tied to the basic_authentication_user, for basic authentication."
        ],
    ),
    "basic_authentication_user": SpecField(
        type=FieldType.string,
        editable=True,
        description=["The user name for basic authentication."],
    ),
}

authentication_spec: dict = {
    "authentication_details": SpecField(
        type=FieldType.dict,
        aliases=["details"],
        suboptions=authentication_details_spec,
        editable=True,
        description=[
            "Includes additional parameters necessary to define basic authentication."
            "If type is set to none, leave this object empty or out of a request."
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        editable=True,
        choices=["none", "basic"],
        description=[
            "The type of authentication in use. This can be None for no authentication, "
            "or basic for authentication using a username and password, "
            "set using the details parameters."
        ],
    ),
}

client_certificate_details_spec: dict = {
    "client_ca_certificate": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The certificate authority (CA) certificate used "
            "to verify a requesting server's identity."
        ],
    ),
    "client_certificate": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The PEM-formatted digital certificate you want to "
            "authenticate requests to your destination with."
        ],
    ),
    "client_private_key": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The private key in the non-encrypted PKCS8 format that authenticates "
            "with the back-end server. If you want to use mutual authentication, "
            "you need to provide both the client_certificate and the client_private_key."
        ],
    ),
    "tls_hostname": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The hostname that verifies the server's certificate "
            "and matches the Subject Alternative Names (SANs) in the certificate. "
            "If not provided, the API fetches the hostname from the endpoint_url."
        ],
    ),
}

custom_headers_spec: dict = {
    "name": SpecField(
        type=FieldType.string,
        editable=True,
        required=True,
        description=[
            "The name of the custom header to include in the request."
        ],
    ),
    "value": SpecField(
        type=FieldType.string,
        editable=True,
        required=True,
        description=[
            "The body content for the custom header to include in the request."
        ],
    ),
}

details_spec: dict = {
    # --- akamai_object_storage fields ---
    "access_key_id": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The unique identifier assigned to the Object Storage key required "
            "for authentication to the bucket. "
            "Run the List Object Storage keys operation and store the id for the applicable key. "
            "(Required for type: akamai_object_storage)"
        ],
    ),
    "access_key_secret": SpecField(
        type=FieldType.string,
        editable=True,
        no_log=True,
        description=[
            "The Object Storage key's secret key. "
            "This is used as a password to validate the key. "
            "(Required for type: akamai_object_storage)"
        ],
    ),
    "bucket_name": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The name of the Object Storage bucket. "
            "Run the List Object Storage buckets operation and store the label "
            "for the target bucket. (Required for type: akamai_object_storage)"
        ],
    ),
    "host": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The hostname where the Object Storage bucket can be accessed. "
            "Run the List Object Storage buckets operation and store the hostname "
            "for the target bucket. (Required for type: akamai_object_storage)"
        ],
    ),
    "path": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "Include this object to set a custom path for audit log storage "
            "in your Object Storage bucket. (Optional for type: akamai_object_storage)"
        ],
    ),
    # --- custom_https fields ---
    "authentication": SpecField(
        type=FieldType.dict,
        suboptions=authentication_spec,
        editable=True,
        description=[
            "Authentication details required to access the endpoint_url. "
            "(Used for type: custom_https)"
        ],
    ),
    "client_certificate_details": SpecField(
        type=FieldType.dict,
        suboptions=client_certificate_details_spec,
        editable=True,
        description=[
            "Contains transport layer security (TLS) client certificate information to "
            "additionally secure the connection for the request. "
            "(Used for type: custom_https)"
        ],
    ),
    "content_type": SpecField(
        type=FieldType.string,
        editable=True,
        choices=["application/json", "application/json; charset=utf-8"],
        description=[
            "The content type for requests to the endpoint_url. "
            "This can be application/json for request bodies formatted as JSON, "
            "or application/json; charset=utf-8 for JSON-format content encoded using UTF-8."
            "(Used for type: custom_https)"
        ],
    ),
    "custom_headers": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=custom_headers_spec,
        editable=True,
        description=[
            "Pairs of parameters used to optionally include custom headers in the request."
            "(Used for type: custom_https)"
        ],
    ),
    "data_compression": SpecField(
        type=FieldType.string,
        editable=True,
        choices=["gzip", "None"],
        description=[
            "Specifies whether data compression is applied to files included in a request. "
            "This can be gzip to apply this compression format or None."
            "(Used for type: custom_https)"
        ],
    ),
    "endpoint_url": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The URL where the request will be sent. (Used for type: custom_https)"
        ],
    ),
}

spec: dict = {
    "details": SpecField(
        type=FieldType.dict,
        suboptions=details_spec,
        editable=True,
        description=[
            "Settings for the destination. "
            "For type 'akamai_object_storage': provide access_key_id, access_key_secret, "
            "bucket_name, host and optionally path. "
            "For type 'custom_https': provide authentication, client_certificate_details, "
            "content_type, data_compression, endpoint_url and optionally custom_headers."
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The name of the destination object. Used for display purposes."
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        editable=True,
        choices=["akamai_object_storage", "custom_https"],
        description=[
            "The type of destination for log data sync, "
            "either akamai_object_storage if Object Storage is the destination, "
            "or custom_https for a unique URL"
        ],
    ),
    "id": SpecField(
        type=FieldType.integer,
        description=[
            "The unique identifier assigned to the logs destination. "
            "Run the List logs destinations operation and store the id "
            "for the applicable logs destination. "
            "Required for updating."
        ],
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
        description=["Wait for the logs destination ready."],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        default=600,
        description=[
            "The amount of time, in seconds, to wait for the logs destination."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Manage logs destination that serves as a sync point for logs data. "
        "You need read_write access to the scope to call this operation."
    ],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "logs_destination": SpecReturnValue(
            description="The logs destination in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-destination",
            type=FieldType.dict,
            sample=docs.result_logs_destination_sample,
        ),
    },
)

# Fields that can be updated on an existing Logs Destination
MUTABLE_FIELDS = {"details", "label", "type"}

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

    def _wait_for_logs_destination_ready(
        self, logs_destination: LogsDestination
    ) -> None:
        def poll_func() -> bool:
            logs_destination._api_get()
            if logs_destination.status == "inactive":
                self.fail(
                    "Logs destination is inactive. Please verify that your credentials, "
                    "host and bucket details are correct."
                )
            return logs_destination.status == "active"

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

    def _get_logs_destination(
        self, destination_id: int
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
            self.register_action("Created logs destination")

            storage_type = params.pop("type")
            if storage_type == "akamai_object_storage":
                return self._create_akamai_object_storage_logs_destination(
                    storage_type
                )
            if storage_type == "custom_https":
                return self._create_custom_https_logs_destination(storage_type)

            return self.fail(
                msg="invalid type or type not provided for logs destination"
            )

        except Exception as exception:
            return self.fail(
                msg="failed to create logs destination: {0}".format(exception)
            )

    def _create_akamai_object_storage_logs_destination(
        self, storage_type: str
    ) -> Optional[LogsDestination]:
        params = self.module.params

        details = params.pop("details")
        return self.client.monitor.destination_create(
            label=params.pop("label"),
            type=storage_type,
            details=AkamaiObjectStorageLogsDestinationDetails(
                access_key_id=details.pop("access_key_id"),
                access_key_secret=details.pop("access_key_secret"),
                bucket_name=details.pop("bucket_name"),
                host=details.pop("host"),
                path=details.pop("path"),
            ),
        )

    def _create_custom_https_logs_destination(
        self, storage_type: str
    ) -> Optional[LogsDestination]:
        params = self.module.params
        details = params.pop("details")
        authentication = details.pop("authentication")

        authentication_details = authentication.pop("authentication_details")
        client_cert_details = details.pop("client_certificate_details")

        custom_headers = [
            CustomHeader(name=h.get("name"), value=h.get("value"))
            for h in (details.pop("custom_headers", None) or [])
        ] or None

        return self.client.monitor.destination_create(
            label=params.pop("label"),
            type=storage_type,
            details=CustomHTTPSLogsDestinationDetails(
                endpoint_url=details.pop("endpoint_url"),
                authentication=DestinationAuthentication(
                    type=authentication.pop("type"),
                    details=BasicAuthenticationDetails(
                        basic_authentication_user=authentication_details.pop(
                            "basic_authentication_user"
                        ),
                        basic_authentication_password=authentication_details.pop(
                            "basic_authentication_password"
                        ),
                    ),
                ),
                data_compression=details.pop("data_compression"),
                content_type=details.pop("content_type"),
                custom_headers=custom_headers,
                client_certificate_details=ClientCertificateDetails(
                    client_ca_certificate=client_cert_details.pop(
                        "client_ca_certificate"
                    ),
                    client_certificate=client_cert_details.pop(
                        "client_certificate"
                    ),
                    client_private_key=client_cert_details.pop(
                        "client_private_key"
                    ),
                    tls_hostname=client_cert_details.pop("tls_hostname"),
                ),
            ),
        )

    def _update_logs_destination(self) -> None:
        """Handles all update functionality for the current Logs Destination"""

        handle_updates(
            self._logs_destination,
            filter_null_values(self.module.params),
            MUTABLE_FIELDS,
            self.register_action,
            diff_overrides={"details": self.__details_diff_override},
        )

        if self.module.params.get("wait"):
            self._wait_for_logs_destination_ready(self._logs_destination)

    @staticmethod
    def __details_diff_override(
        key: str, old_value: Any, new_value: Any
    ) -> tuple[bool, Any]:
        result = new_value.copy()

        # Remove write-only secrets before comparing
        compare_new_value = new_value.copy()
        if "access_key_secret" in compare_new_value:
            del compare_new_value["access_key_secret"]

        compare_old_value = (
            old_value.copy() if isinstance(old_value, dict) else {}
        )
        if "access_key_secret" in compare_old_value:
            del compare_old_value["access_key_secret"]

        return compare_old_value != compare_new_value, result

    def _handle_logs_destination(self) -> None:
        params = self.module.params

        destination_id: int = params.get("id")

        if destination_id:
            self._logs_destination = self._get_logs_destination(destination_id)

        # Create logs destination if it does not already exist
        if self._logs_destination is None:
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
    """Constructs and call the Linode Monitor Logs Destination module"""
    LinodeLogsDestination()


if __name__ == "__main__":
    main()
