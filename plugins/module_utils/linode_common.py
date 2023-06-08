"""This module contains the base Linode module that other modules inherit from."""

from __future__ import absolute_import, division, print_function

import traceback
from typing import Any, Type

import polling
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    format_api_error,
    format_generic_error,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_timeout import (
    TimeoutContext,
)

try:
    from ansible.module_utils.ansible_release import (
        __version__ as ANSIBLE_VERSION,
    )
except Exception:
    ANSIBLE_VERSION = "unknown"

from ansible.module_utils.basic import (
    AnsibleModule,
    env_fallback,
    missing_required_lib,
)

try:
    from linode_api4 import ApiError
    from linode_api4 import Base as LinodeAPIType
    from linode_api4 import (
        Image,
        IPAddress,
        LinodeClient,
        MySQLDatabase,
        PersonalAccessToken,
        PostgreSQLDatabase,
        SSHKey,
        StackScript,
        UnexpectedResponseError,
    )

    HAS_LINODE = True
except ImportError:
    HAS_LINODE = False
    HAS_LINODE_EXC = traceback.format_exc()

COLLECTION_USER_AGENT = (
    "ansible_linode (https://github.com/linode/ansible_linode) "
    f"Ansible/{ANSIBLE_VERSION}"
)

LINODE_COMMON_ARGS = {
    "api_token": {
        "type": "str",
        "fallback": (env_fallback, ["LINODE_API_TOKEN", "LINODE_TOKEN"]),
        "required": True,
        "no_log": True,
    },
    "api_version": {
        "type": "str",
        "fallback": (env_fallback, ["LINODE_API_VERSION"]),
        "default": "v4",
    },
    "state": {
        "type": "str",
        "required": True,
        "choices": ["present", "absent"],
    },
    "ua_prefix": {
        "type": "str",
        "description": "An HTTP User-Agent Prefix to prepend in API requests.",
        "doc_hide": True,
        "fallback": (env_fallback, ["LINODE_UA_PREFIX"]),
    },
}

LINODE_TAG_ARGS = {
    "tags": {
        "type": "list",
        "description": "The tags to assign to this resource.",
    },
}

LINODE_LABEL_ARGS = {
    "label": {
        "type": "str",
        "required": True,
        "description": "The label to assign to this resource.",
    },
}

RESOURCE_NAMES = (
    {
        Image: "image",
        MySQLDatabase: "MySQL database",
        PersonalAccessToken: "personal access token",
        PostgreSQLDatabase: "PostgreSQL database",
        SSHKey: "SSH key",
        StackScript: "stackscript",
        IPAddress: "IP address",
    }
    if HAS_LINODE
    else {}
)

MAX_RETRIES = 5
RETRY_INTERVAL_SECONDS = float(4)
RETRY_STATUSES = {408, 429, 502}


class LinodeModuleBase:
    """A base for all Linode resource modules."""

    def __init__(
        self,
        module_arg_spec: dict,
        supports_tags: bool = True,
        has_label: bool = True,
        bypass_checks: bool = False,
        no_log: bool = False,
        mutually_exclusive: Any = None,
        required_together: Any = None,
        required_one_of: Any = None,
        add_file_common_args: bool = False,
        supports_check_mode: bool = False,
        required_if: Any = None,
        skip_exec: bool = False,
    ) -> None:
        arg_spec = {}
        arg_spec.update(LINODE_COMMON_ARGS)

        if has_label:
            arg_spec.update(LINODE_LABEL_ARGS)

        if supports_tags:
            arg_spec.update(LINODE_TAG_ARGS)

        arg_spec.update(module_arg_spec)

        self._client = None

        self.module = AnsibleModule(
            argument_spec=arg_spec,
            bypass_checks=bypass_checks,
            no_log=no_log,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
            required_one_of=required_one_of,
            add_file_common_args=add_file_common_args,
            supports_check_mode=supports_check_mode,
            required_if=required_if,
        )

        self.results: dict = self.results or {"changed": False, "actions": []}

        # This field may or may not be present depending on the module
        timeout_param = self.module.params.get("wait_timeout", 120)

        self._timeout_ctx: TimeoutContext = TimeoutContext(
            timeout_seconds=timeout_param
        )

        if not HAS_LINODE:
            self.fail(
                msg=missing_required_lib("linode_api4"),
                exception=HAS_LINODE_EXC,
            )

        if not skip_exec:
            try:
                res = self.exec_module(**self.module.params)
            except ApiError as err:
                # We don't want to return a stack trace for an API error
                self.fail(msg=format_api_error(err))
            except polling.TimeoutException as err:
                self.fail(
                    msg="failed to wait for condition: timeout period expired"
                )
            except (
                ValueError,
                RuntimeError,
                UnexpectedResponseError,
                TypeError,
                IndexError,
            ) as err:
                self.fail(msg=format_generic_error(err))

            self.module.exit_json(**res)

    def fail(self, msg: str, **kwargs: Any) -> None:
        """
        Shortcut for calling module.fail

        :param msg: Error message
        :param kwargs: Any key=value pairs
        :return: None
        """
        self.module.fail_json(msg=msg, **kwargs)

    def exec_module(self, **kwargs: Any) -> Any:
        """Returns a not implemented error"""
        self.fail(
            "Error: module {0} not implemented".format(self.__class__.__name__)
        )

    def register_action(self, description: str) -> None:
        """Sets the changed flag to true and adds the given action to the result"""

        self.results["changed"] = True
        self.results["actions"].append(description)

    def _get_resource_by_id(
        self, resource_type: Type[LinodeAPIType], resource_id: int
    ):
        try:
            resource = resource_type(self.client, resource_id)
            resource._api_get()
            return resource
        except Exception as exception:
            resource_name = (
                RESOURCE_NAMES.get(resource_type)
                or type(resource_type).__name__
            )
            return self.fail(
                msg=f"failed to get {resource_name} "
                "with id {resource_id}: {exception}"
            )

    @property
    def client(self) -> LinodeClient:
        """Creates a 'client' property that is used to access the Linode API."""
        if not self._client:
            api_token = self.module.params["api_token"]
            api_version = self.module.params["api_version"]

            user_agent = COLLECTION_USER_AGENT

            # Allow for custom user-agent prefixes
            ua_prefix = self.module.params["ua_prefix"]
            if ua_prefix is not None:
                user_agent = f"{ua_prefix}  {user_agent}"

            self._client = LinodeClient(
                api_token,
                base_url="https://api.linode.com/{0}".format(api_version),
                user_agent=user_agent,
                retry_rate_limit_interval=RETRY_INTERVAL_SECONDS,
                retry_max=MAX_RETRIES,
                retry_statuses=RETRY_STATUSES,
            )

        return self._client
