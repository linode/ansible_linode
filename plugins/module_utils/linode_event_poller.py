"""
Contains a helper class for polling for resource events.
"""

from typing import Dict, Any, List, Optional

import polling
from linode_api4 import LinodeClient, Event

from ansible_collections.linode.cloud.plugins.module_utils.linode_timeout import TimeoutContext


POLL_INTERVAL_SECONDS = 2


class EventPoller:
    """
    EventPoller allows modules to dynamically poll for Linode events
    """

    def __init__(self, client: LinodeClient, entity_type: str, action: str, entity_id: int = None):
        self._client = client
        self._entity_type = entity_type
        self._entity_id = entity_id
        self._action = action

        # Initialize with an empty cache if no entity is specified
        if self._entity_id is None:
            self._previous_event_cache = {}
            return

        # We only want the first page of this response
        result = client.get('/account/events', filters=self._build_filter())

        self._previous_event_cache = {v['id']: v for v in result['data']}

    def _build_filter(self) -> Dict[str, Any]:
        """Generates a filter dict to use in HTTP requests"""
        return {
            '+order': 'asc',
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

    def _attempt_merge_event_into_cache(self, event: Dict[str, Any]):
        """
        Attempts to merge the given event into the event cache.
        """

        if event['id'] in self._previous_event_cache:
            return

        self._previous_event_cache[event['id']] = event

    def _check_has_new_event(self, events: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        If a new event is found in the given list, return it.
        """

        for event in events:
            # Ignore cached events
            if event['id'] in self._previous_event_cache:
                continue

            return event

        return None

    def wait_for_next_event(self, timeout: int) -> Event:
        """
        Waits for and returns the next event matching the
        poller's configuration.
        """
        result_event: Dict[str, Any] = {}

        def poll_func():
            new_event = self._check_has_new_event(
                self._client.get('/account/events', filters=self._build_filter())['data']
            )

            event_exists = new_event is not None

            if event_exists:
                nonlocal result_event
                result_event = new_event
                self._attempt_merge_event_into_cache(new_event)

            return event_exists

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


def wait_for_resource_free(client: LinodeClient, entity_type: str, entity_id: int, timeout: int):
    """
    Waits for all events relevant events to not be scheduled or in-progress.
    """

    timeout_ctx = TimeoutContext(timeout_seconds=timeout)

    filter = {
        '+order': 'desc',
        '+order_by': 'created',
        'entity.id': entity_id,
        'entity.type': entity_type,
    }

    def poll_func():
        events = client.get('/account/events', filters=filter)['data']
        for event in events:
            if event['status'] in ('scheduled', 'started'):
                return False

        return True

    if poll_func():
        return

    polling.poll(
        poll_func,
        step=POLL_INTERVAL_SECONDS,
        timeout=timeout_ctx.seconds_remaining,
    )