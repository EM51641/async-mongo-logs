import logging
from queue import Queue  # type: ignore


class QueueHandler(logging.Handler):
    """
    A custom logging handler that puts log messages into a queue.

    Args:
        level (int): The logging level for the handler.
        queue (Queue): The queue to put log messages into.

    Attributes:
        queue (Queue): The queue to put log messages into.

    """

    def __init__(self, queue: Queue):
        """
        Initializes a QueueHandler object.

        Args:
            level (int): The logging level for the handler.
            queue (Queue): The queue to which log records will be pushed.

        Returns:
            None
        """
        super().__init__()
        self.queue = queue

    def emit(self, record):
        """
        Emit a log record by putting it into the queue.

        Args:
            record (LogRecord): The log record to emit.

        """
        self.queue.put(record)
