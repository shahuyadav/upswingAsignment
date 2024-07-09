from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from datetime import datetime
import toml

from path import APP_PATH

"""make required variables from settings
"""
SETTINGS_PATH = APP_PATH + 'settings.toml'
settings = toml.load(SETTINGS_PATH)
my_db_host = settings['db']['host']
my_db_port = settings['db']['port'] #27017
my_db = settings['db']['db'] #'mqtt_data'
my_db_collection = settings['db']['collection'] #'numbers'

"""make mongo db
    """
mongo_client = MongoClient(my_db_host, my_db_port)
db = mongo_client[my_db]
collection = db[my_db_collection]

"""make FastAPI object
    """
app = FastAPI()

class Message(BaseModel):
    topic: str
    message: int
    timestamp: datetime

"""endpoint to get data from db
    """
@app.get("/data", response_model=List[Message])
async def get_data(start_time: datetime = Query(...), end_time: datetime = Query(...)):
    query = {
        "timestamp": {
            "$gte": start_time,
            "$lte": end_time
        }
    }
    cursor = collection.find(query)
    results = [Message(**doc) for doc in cursor]
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
