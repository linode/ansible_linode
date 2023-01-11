import datetime


class TimeoutContext:
    def __init__(self, timeout_seconds=120):
        self._start_time = datetime.datetime.now()
        self._timeout_seconds = timeout_seconds

    def start(self, start_time=datetime.datetime.now()):
        """Sets the timeout start time to the current time"""
        self._start_time = start_time

    def extend(self, seconds):
        self._timeout_seconds += seconds

    @property
    def expired(self):
        return self.seconds_remaining > self._timeout_seconds

    @property
    def valid(self):
        return not self.expired

    @property
    def seconds_remaining(self):
        return (datetime.datetime.now() - self._start_time).seconds
