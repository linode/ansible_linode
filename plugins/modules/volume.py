#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Volumes."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
from typing import Any, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.volume as docs
import polling
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_event_poller import (
    EventPoller,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    request_retry,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Volume

linode_volume_spec = dict(
    label=SpecField(
        type=FieldType.string,
        description=[
            "The Volume’s label, which is also used in the "
            "filesystem_path of the resulting volume."
        ],
    ),
    config_id=SpecField(
        type=FieldType.integer,
        default=None,
        description=[
            "When creating a Volume attached to a Linode, the ID of the Linode Config "
            "to include the new Volume in."
        ],
    ),
    linode_id=SpecField(
        type=FieldType.integer,
        default=None,
        editable=True,
        description=[
            "The Linode this volume should be attached to upon creation.",
            "If not given, the volume will be created without an attachment.",
        ],
    ),
    region=SpecField(
        type=FieldType.string,
        description=[
            "The location to deploy the volume in.",
            "See U(https://api.linode.com/v4/regions)",
        ],
    ),
    size=SpecField(
        type=FieldType.integer,
        default=None,
        editable=True,
        description=[
            "The size of this volume, in GB.",
            "Be aware that volumes may only be resized up after creation.",
        ],
    ),
    attached=SpecField(
        type=FieldType.bool,
        default=True,
        editable=True,
        description=[
            "If true, the volume will be attached to a Linode. "
            "Otherwise, the volume will be detached."
        ],
    ),
    wait_timeout=SpecField(
        type=FieldType.integer,
        default=240,
        description=[
            "The amount of time, in seconds, to wait for a volume to "
            "have the active status."
        ],
    ),
    state=SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    source_volume_id=SpecField(
        type=FieldType.integer,
        required=False,
        description=["The volume id of the desired volume to clone."],
    ),
    tags=SpecField(
        type=FieldType.list,
        required=False,
        description=["The tags to be attached to the volume."],
    ),
)

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode Volume."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_volume_spec,
    examples=docs.specdoc_examples,
    return_values=dict(
        volume=SpecReturnValue(
            description="The volume in JSON serialized form.",
            docs_url="https://www.linode.com/docs/api/volumes/#volume-view__responses",
            type=FieldType.dict,
            sample=docs.result_volume_samples,
        )
    ),
)


class LinodeVolume(LinodeModuleBase):
    """Module for creating and destroying Linode Volumes"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of = ["state", "label"]
        self.results = dict(
            changed=False,
            actions=[],
            volume=None,
        )

        self._volume: Optional[Volume] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_volume_by_label(self, label: str) -> Optional[Volume]:
        try:
            return self.client.volumes(Volume.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get volume {0}: {1}".format(label, exception)
            )

    def _create_volume(self) -> Optional[Volume]:
        params = self.module.params
        label = params.pop("label")
        region = params.pop("region")
        linode_id = params.pop("linode_id")
        size = params.pop("size")

        try:
            return self.client.volume_create(
                label, region, linode_id, size, **params
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create volume: {0}".format(exception)
            )

    def _wait_for_volume_status(
        self, volume: Volume, status: Set[str], timeout: int
    ) -> None:
        def poll_func() -> bool:
            volume._api_get()
            return volume.status in status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=5,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail(
                "failed to wait for volume status: timeout period expired"
            )

    def _wait_for_volume_active(self, volume: Volume) -> None:
        self._wait_for_volume_status(
            volume, {"active"}, self._timeout_ctx.seconds_remaining
        )

    def _clone_volume(self) -> Volume:
        params = self.module.params

        source_id = params.get("source_volume_id")
        source_volume = Volume(self.client, source_id)
        source_volume._api_get()  # Force lazy-loading

        # Check if source volume was found
        if source_volume is None:
            return self.fail(
                msg="Volume with is {0} could not be found.".format(source_id)
            )

        # If regions don't match up, it is an invalid clone operation
        if params.get("region") != source_volume.region.id:
            return self.fail(
                msg="Specified region does not match source volume region."
            )

        # Perform the clone operation
        vol = request_retry(
            lambda: self.client.post(
                "/volumes/{}/clone".format(source_id),
                data={"label": params.get("label")},
            )
        )

        cloned_volume = Volume(self.client, vol.get("id"))
        cloned_volume._api_get()  # Force lazy-loading

        return cloned_volume

    def _handle_volume(self) -> None:
        params = self.module.params

        label: str = params.get("label")
        size: int = params.get("size")
        linode_id: int = params.get("linode_id")
        config_id: int = params.get("config_id")
        attached: bool = params.pop("attached")

        self._volume = self._get_volume_by_label(label)

        # Create the volume if it does not already exist or
        # clone if source volume id was provided
        if self._volume is None:
            if params.get("source_volume_id") is not None:
                self._volume = self._clone_volume()
                self.register_action(
                    "Cloned volume {0} with source id {1}".format(
                        label, params.get("source_volume_id")
                    )
                )
            else:
                self._volume = self._create_volume()
                self.register_action("Created volume {0}".format(label))

        # Ensure volume is active before continuing
        self._wait_for_volume_active(self._volume)

        # Resize the volume if its size does not match
        if size is not None and self._volume.size != size:
            self._volume.resize(size)
            self.register_action(
                "Resized volume {0} to size {1}".format(label, size)
            )

            # Wait for resize to complete
            self._wait_for_volume_active(self._volume)

        # Attach the volume to a Linode
        if linode_id is not None and self._volume.linode_id != linode_id:
            attach_poller = EventPoller(
                self.client,
                "volume",
                "volume_attach",
                entity_id=self._volume.id,
            )

            self._volume.attach(linode_id, config_id)
            self.register_action(
                "Attached volume {0} to linode_id {1} and config_id {2}".format(
                    label, linode_id, config_id
                )
            )

            attach_poller.wait_for_next_event_finished(
                self._timeout_ctx.seconds_remaining
            )

        if not attached:
            detach_poller = EventPoller(
                self.client,
                "volume",
                "volume_detach",
                entity_id=self._volume.id,
            )

            self._volume.detach()
            self.register_action("Detached volume {0}".format(label))

            detach_poller.wait_for_next_event_finished(
                self._timeout_ctx.seconds_remaining
            )

        # Force lazy-loading
        self._volume._api_get()

        self.results["volume"] = self._volume._raw_json

    def _handle_volume_absent(self) -> None:
        label: str = self.module.params.get("label")

        self._volume = self._get_volume_by_label(label)

        if self._volume is not None:
            self.results["volume"] = self._volume._raw_json
            self._volume.delete()
            self.register_action("Deleted volume {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for volume module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_volume_absent()
            return self.results

        self._handle_volume()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Volume module"""
    LinodeVolume()


if __name__ == "__main__":
    main()
