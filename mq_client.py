"""make required imports
"""
import paho.mqtt.client as mqtt
import random
import time
import toml

# local imports
from path import APP_PATH


"""make required variables from settings
"""
SETTINGS_PATH = APP_PATH + 'settings.toml'
settings = toml.load(SETTINGS_PATH)
my_broker = settings['mqtt']['broker'] #'broker.hivemq.com'
my_port = settings['mqtt']['port'] #1883
my_topic = settings['mqtt']['topic'] #'my_topic/status'
sec_delay = settings['time']['sec_delay'] #1

"""make mqtt object
"""
client = mqtt.Client()

"""connect mqtt client
"""
client.connect(my_broker, my_port, 60)

"""make method to publich random numner
"""
def publish_rand_num(rand_num):    
    pub_info = client.publish(my_topic, rand_num)   
    print(print(f"publish status: {pub_info}"))

"""publish in while with set delay
"""
try:
    while True:
        rand_num = random.randint(1, 6)
        publish_rand_num(rand_num=rand_num)        
        time.sleep(sec_delay)
except KeyboardInterrupt:
    print("Exit client due to keyboard interrupt")

client.disconnect()
