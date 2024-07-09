"""make required imports
"""
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import toml
import datetime
# local imports
from path import APP_PATH

"""make required variables from settings
"""
SETTINGS_PATH = APP_PATH + 'settings.toml'
settings = toml.load(SETTINGS_PATH)
my_broker = settings['mqtt']['broker'] #'broker.hivemq.com'
my_port = settings['mqtt']['port'] #1883
my_topic = settings['mqtt']['topic'] #'my_topic/status'


my_db_host = settings['db']['host']
my_db_port = settings['db']['port'] #27017
my_db = settings['db']['db'] #'mqtt_data'
my_db_collection = settings['db']['collection'] #'numbers'

"""make mongo db
    """
mongo_client = MongoClient(my_db_host, my_db_port)
db = mongo_client[my_db]
collection = db[my_db_collection]

"""connect to db on mqtt connect
    """
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")   
    client.subscribe(my_topic)

"""insert data in db when mqtt server gets data
    """
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")   
    try:
        data = {
            "topic": msg.topic,
            "message": int(msg.payload.decode()),
            "timestamp": datetime.datetime.now()
        }
        collection.insert_one(data)
        print("Data stored in MongoDB")
    except Exception as e:
        print(f"Failed to store data in MongoDB: {e}")

try:
    """create mqtt client with callback methods to connect and insert data in db
        """
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    """connect to same broker as client 
        """
    mqtt_client.connect(my_broker, my_port, 60)

    mqtt_client.loop_forever()
except KeyboardInterrupt:
    mongo_client.close()
    mqtt_client.loop_stop(force=True)
    mqtt_client.disconnect()

