from __future__ import annotations

import asyncio
from queue import Queue  # type: ignore
from threading import Thread
from typing import Any, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection  # type: ignore
from pydantic import BaseModel  # type: ignore

T = TypeVar("T", bound=BaseModel)


class AsyncQueueListener:
    """
    Custom queue listener class that extends the default QueueListener class
    from the logging module.
    """

    def __init__(
        self,
        queue: Queue,
        entity: type[T],
        collection_ref: AsyncIOMotorCollection,
        autorun=True,
    ) -> None:
        """
        Initialize the Logger object.

        Args:
            queue (Queue):
                The queue to store log messages.
            entity (type[T]):
                The type of entity being logged.
            collection_ref (AsyncIOMotorCollection):
                The reference to the MongoDB collection.
            autorun (bool, optional):
                Whether to start the logger automatically. Defaults to True.
        """
        self.queue = queue
        self.entity = entity
        self.collection_ref = collection_ref

        if autorun:
            self.start()

    def start(self):
        """
        Starts the logger and continuously saves logs to the database.
        """
        self._thread = Thread(target=self._run_event_loop)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        """
        Stop the listener.

        This asks the thread to terminate, and then waits for it to do so.
        Note that if you don't call this before your application exits, there
        may be some records still left on the queue, which won't be processed.
        """
        if self._thread:
            self._thread.join()
            self._thread = None

    def dequeue(self, block=False) -> Any:
        """
        Removes and returns the next record from the queue.

        Returns:
            The next record from the queue.
        """
        record = self.queue.get(block=block)
        return record

    def _run_event_loop(self):
        """
        Runs the event loop for the QueueListener.

        This method creates a new event loop, sets it as the current event loop
        and runs the event loop indefinitely. It also creates a task to monitor
        the queue and adds it to the event loop.

        Note: This method is intended to be called internally and should not be
        called directly from outside the class.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._monitor())

    async def _monitor(self):
        """
        Monitors the queue and saves logs to the database.
        """
        while True:
            record = self.dequeue(block=True)
            await self._save_log_to_db(record)

    async def _save_log_to_db(self, record: Any) -> None:
        """
        Saves the log record to the database.

        Args:
            record (Any): The log record to be saved.

        Returns:
            None
        """
        keys = self.entity.model_fields.keys()
        values = {key: getattr(record, key, None) for key in keys}
        log = self.entity(**values)
        data = log.model_dump()
        await self.collection_ref.insert_one(data)
