# upswingAsignment
upswing assignment for python backend developer 
# MQTT Client-Server with FastAPI and MongoDB

This project demonstrates an MQTT client-server application with a FastAPI backend to interact with MongoDB.

## Prerequisites

- Python 3.7+
- MongoDB
- MQTT Broker (e.g., broker.hivemq.com)

## Setup

1. **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Settings**

    Create a `settings.toml` file in the project root directory with the following content:

    ```toml
    [mqtt]
    broker = "broker.hivemq.com"
    port = 1883
    topic = "my_topic/status"

    [db]
    host = "localhost"
    port = 27017
    db = "mqtt_data"
    collection = "numbers"
    ```

4. **Run the MQTT Server**

    ```bash
    python server.py
    ```

5. **Run the FastAPI Application**

    ```bash
    python fastapi.py
    ```

6. **Send MQTT Messages**

    Use the `client.py` script to send messages to the MQTT broker:

    ```bash
    python client.py
    ```

## Endpoints

### GET /data

Retrieve data from MongoDB between specified start and end times.

#### Query Parameters:

- `start_time` (datetime): Start time for the data query.
- `end_time` (datetime): End time for the data query.

#### Example:

```bash
curl -X GET "http://127.0.0.1:8000/data?start_time=2023-01-01T00:00:00&end_time=2023-12-31T23:59:59"

