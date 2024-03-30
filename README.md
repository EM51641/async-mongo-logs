# MongoLogs

MongoLogs is a project designed to help python developers to log asynchronously on MongoDB.

## Features

- Asynchronous logging
- Easy integration with MongoDB
- Runtime Checking of our logs using pydantic

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Installation

To install AsyncMongoLogger, follow these steps:

```bash
# Clone the repository
git clone https://github.com/EM51641/async-mongo-logs.git

# Navigate into the cloned repository
cd async-mongo-logs

# Install the project dependencies with Poetry
poetry install
```

### Prerequisites

- Python 3.8 or higher
- Poetry (Python dependency management tool)
- Docker and Docker Compose
- MongoDB

### Examples

Here's an example of how to use MongoLogs:

```python
import logging
from pydantic import BaseModel
from mongologs.app import AsyncLogger

MONGO_URI = "mongodb://mongo:mongo@mongo/mongo"

# Define a log entity
class LogEntity(BaseModel):
    message: str

# Create an AsyncLogger instance
app = AsyncLogger(entity=LogEntity, mongo_uri=MONGO_URI)

# Get a logger and add the AsyncLogger's handler to it
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(app.queue_handler)

# Log a message
logger.debug('This is a debug message')

```

In this example, we first connect to MongoDB and drop the 'mongologs' database if it exists. Then we define a log entity and create an AsyncLogger instance.

## Running the Tests

To run the tests, you need to start the MongoDB service and then use pytest. Here's how you can do it:

```bash
# Start the MongoDB service using Docker Compose
docker-compose up -d

# Run the tests using pytest
poetry run pytest
```
