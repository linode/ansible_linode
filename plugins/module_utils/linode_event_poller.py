"""
Contains a helper class for polling for resource events.
"""

from typing import Dict, Any

import polling
from linode_api4 import LinodeClient, Event

from ansible_collections.linode.cloud.plugins.module_utils.linode_timeout import TimeoutContext


POLL_INTERVAL_SECONDS = 2


class EventPoller:
    """
    EventPoller allows modules to dynamically poll for Linode events
    """

    def __init__(self, client: LinodeClient, entity_type: str, action: str, entity_id: int = 0):
        self._client = client
        self._entity_type = entity_type
        self._entity_id = entity_id
        self._action = action

        # Initialize with an empty cache if no entity is specified
        if self._entity_id == 0:
            self._previous_event_cache = {}
            return

        # We only want the first page of this response
        result = client.get('/account/events', filters=self._build_filter())

        self._previous_event_cache = {v['id']: v for v in result['data']}

    def _build_filter(self) -> Dict[str, Any]:
        """Generates a filter dict to use in HTTP requests"""
        return {
            '+order': 'desc',
            '+order_by': 'created',
            'entity.id': self._entity_id,
            'entity.type': self._entity_type,
            'action': self._action
        }

    def set_entity_id(self, entity_id: int) -> None:
        """
        Sets the ID of the entity to filter on.
        This is useful for create operations where
        the entity id might not be known in __init__.
        """
        self._entity_id = entity_id

    def wait_for_next_event(self, timeout: int) -> Event:
        """
        Waits for and returns the next event matching the
        poller's configuration.
        """
        result_event: Dict[str, Any] = {}

        def poll_func():
            result = self._client.get('/account/events', filters=self._build_filter())
            for event in result['data']:
                if event['id'] in self._previous_event_cache:
                    continue

                nonlocal result_event
                result_event = event

                # Merge the new events into the cache
                for event in result['data']:
                    if event['id'] in self._previous_event_cache:
                        continue

                    self._previous_event_cache[event['id']] = event

                return True

            return False

        if poll_func():
            return Event(self._client, result_event['id'], json=result_event)

        polling.poll(
            poll_func,
            step=POLL_INTERVAL_SECONDS,
            timeout=timeout,
        )

        return Event(self._client, result_event['id'], json=result_event)

    def wait_for_next_event_finished(self, timeout: int):
        """
        Waits for the next event to enter status `finished` or `notification`.
        """

        timeout_ctx = TimeoutContext(timeout_seconds=timeout)
        event = self.wait_for_next_event(timeout_ctx.seconds_remaining)

        def poll_func():
            event._api_get()
            return event.status in ['finished', 'notification']

        if poll_func():
            return event

        polling.poll(
            poll_func,
            step=POLL_INTERVAL_SECONDS,
            timeout=timeout_ctx.seconds_remaining,
        )

        return event
