import logging

import pytest  # type: ignore
from pydantic import BaseModel
from pymongo import MongoClient

from mongologs.app import AsyncLogger


@pytest.fixture(autouse=True)
def db():
    """
    Set up the handler for logging.

    Returns:
        The queue handler for the logging application.
    """

    db = MongoClient(
        host="mongodb://mongo:mongo@localhost:27017/mongo?authSource=admin"
    )

    if "mongologs" in db.list_database_names():
        db.drop_database("mongologs")

    return db


@pytest.fixture
def basic_handler(db):
    """
    Set up the handler for logging.

    Returns:
        The queue handler for the logging application.
    """

    class LogEntity(BaseModel):
        message: str  # type: ignore

    app = AsyncLogger(
        entity=LogEntity,
        mongo_uri="mongodb://mongo:mongo@localhost:27017/mongo?authSource=admin",  # type: ignore
    )

    queue_handler = app.queue_handler
    return queue_handler


@pytest.fixture
def logger(basic_handler):
    """
    Returns a list of loggers to test.

    Returns:
        list:
            A list of loggers to test.
    """
    logger = logging.getLogger("pytest")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(basic_handler)
    yield logger
    logger.removeHandler(basic_handler)


@pytest.fixture
def log_collection(db: MongoClient):
    """
    Returns the database collection.

    Returns:
        AsyncIOMotorCollection: The database collection.
    """
    return db.get_database("mongologs").get_collection("logs")
