import asyncio
import logging

import pytest
from pymongo.collection import Collection


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "log_level, message, expected_query",
    [
        (
            logging.DEBUG,
            "This is a debug message",
            {"message": "This is a debug message"},
        ),  # noqa
        (
            logging.INFO,
            "This is an info message",
            {"message": "This is an info message"},
        ),  # noqa
        (
            logging.WARNING,
            "This is a warning message",
            {"message": "This is a warning message"},
        ),  # noqa
        (
            logging.ERROR,
            "This is an error message",
            {"message": "This is an error message"},
        ),  # noqa
        (
            logging.CRITICAL,
            "This is a critical message",
            {"message": "This is a critical message"},
        ),  # noqa
    ],
)
async def test_basic_login(
    logger: logging.Logger,
    log_collection: Collection,
    log_level: int,
    message: str,
    expected_query: dict,
):
    """
    This function is used to test the logging functionality.

    Args:
        setup_handler (QueueHandler): The setup handler for logging.
        collection (AsyncIOMotorCollection): The collection to query.

    Returns:
        None
    """
    logger.log(log_level, message)
    await asyncio.sleep(0.1)

    documents = list(log_collection.find(expected_query))

    assert len(documents) == 1
    assert documents[0]["message"] == message
