from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
from queue import Queue  # type: ignore
from typing import Generic, TypeVar

from motor.motor_asyncio import (  # type: ignore
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
)
from pydantic import BaseModel  # type: ignore

from mongologs.QueueHandler import QueueHandler
from mongologs.QueueListener import AsyncQueueListener

T = TypeVar("T", bound=BaseModel)


class BaseAsyncLogger(Generic[T], ABC):
    """
    Abstract class for configuring an Asynchronous logger
    linked to a NoSQL database.
    """

    def __init__(self, entity: type[T], mongo_uri: str) -> None:
        """
        Initialize a new instance of the App class.

        Args:
            entity (type[T]): The type of entity to work with.
            mongo_uri (str): The MongoDB connection URI.

        Returns:
            None
        """
        self._entity = entity
        self._client = AsyncIOMotorClient(mongo_uri)

    @property
    def entity(self) -> type[T]:
        """
        Gets the entity type.

        Returns:
            type[T]: The entity type.
        """
        return self._entity

    @property
    def client(self) -> AsyncIOMotorClient:
        """
        Gets the MongoDB client.

        Returns:
            AsyncIOMotorClient: The MongoDB client.
        """
        return self._client

    @cached_property
    @abstractmethod
    def queue_handler(self) -> QueueHandler:
        """Not implemented yet."""


class AsyncLogger(BaseAsyncLogger):
    """
    Configures an Asynchronous logger linked to a NoSQL database.
    This class that provides methods for initializing the database.
    """

    @cached_property
    def queue_handler(self) -> QueueHandler:
        """
        Gets the queue handler.

        Returns:
            QueueHandler: The queue handler.
        """
        queue_handler = self._setup_queue_handler_and_listener()
        return queue_handler

    def _setup_queue_handler_and_listener(self) -> QueueHandler:
        """
        Set up the queue handler.

        Returns:
            QueueHandler: The queue handler.
        """
        queue = Queue(-1)  # type: ignore
        queue_handler = QueueHandler(queue)  # type: ignore

        collection = self._setup_collection()
        self._setup_queue_listener(queue, collection)
        return queue_handler

    def _setup_collection(self) -> AsyncIOMotorCollection:
        """
        Set up the database connection.

        Returns:
            AsyncIOMotorClient: The database client.
        """
        db = self._client.get_database("mongologs")
        collection = db.get_collection("logs")
        return collection

    def _setup_queue_listener(
        self, queue: Queue, collection: AsyncIOMotorCollection
    ) -> None:
        """
        Set up the queue listener.

        Args:
            queue (Queue): The queue to listen to.
            collection (AsyncIOMotorCollection): The MongoDB collection.

        Returns:
            AsyncQueueListener: The queue listener.
        """
        queue_listener = AsyncQueueListener(
            queue, self._entity, collection, autorun=False  # type: ignore
        )
        queue_listener.start()
