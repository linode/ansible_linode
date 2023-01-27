"""
This module holds various utilities for managing module polling timeouts.
"""

import datetime


class TimeoutContext:
    """
    TimeoutContext should be used by polling resources to track their provisioning time.
    """

    def __init__(self, timeout_seconds=120):
        self._start_time = datetime.datetime.now()
        self._timeout_seconds = timeout_seconds

    def start(self, start_time=datetime.datetime.now()):
        """Sets the timeout start time to the current time."""
        self._start_time = start_time

    def extend(self, seconds):
        """Extends the timeout window."""
        self._timeout_seconds += seconds

    @property
    def expired(self):
        """Whether the current timeout period has been exceeded."""
        return self.seconds_remaining < 0

    @property
    def valid(self):
        """Whether the current timeout period has not been exceeded."""
        return not self.expired

    @property
    def seconds_remaining(self):
        """The number of seconds until the timeout period has expired."""
        return self._timeout_seconds - (datetime.datetime.now() - self._start_time).seconds
