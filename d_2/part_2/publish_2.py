from cryptography.fernet import Fernet
import paho.mqtt.client as paho
import time
import json
import os
from datetime import datetime

os.system("clear")
print("Part 2: Publish")

# Generate a random encryption key
key = "iHW-wSFTCFb1I2_7ZZWPfDpyP5ntoEVwWmltThQuaz8="

# the_broker = "broker.mqttdashboard.com"
# the_broker = "mqtt.eclipseprojects.io"
# the_broker = "test.mosquitto.org"
the_broker = "broker.emqx.io"

def encrypt_message(message):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    payload = {
        "message": encrypted_message.decode(),  # Convert bytes to string
        "timestamp": datetime.now().isoformat()  # Add a timestamp to the payload
    }
    return json.dumps(payload)

def on_publish(client, userdata, mid):
    print("Published message with MID: " + str(mid))
    if userdata is not None:
        payload = json.loads(userdata)
        print("Latency time: " + str(payload["latency_time"]))

client = paho.Client()
client.on_publish = on_publish

client.connect(the_broker, 1883)
client.loop_start()

count = 0

while True:
    count += 1
    message = "with MID: " + str(count)
    try:
        encrypted_message = encrypt_message(message)
        (rc, mid) = client.publish('messages/topic', encrypted_message, qos=1)
        time.sleep(5)
    except Exception as e:
        print("An error occurred while encrypting or publishing the message:")
        print(str(e))
        break

client.loop_stop()
client.disconnect()
