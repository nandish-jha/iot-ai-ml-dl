from cryptography.fernet import Fernet
import paho.mqtt.client as paho
from datetime import datetime
import socket
import json
import time

print("Publishing from own PC\n")

# Generate a random encryption key
key = "iHW-wSFTCFb1I2_7ZZWPfDpyP5ntoEVwWmltThQuaz8="

# the_broker = "broker.mqttdashboard.com"
# the_broker = "mqtt.eclipseprojects.io"
# the_broker = "test.mosquitto.org"
the_broker = "broker.emqx.io"

hostname = socket.gethostname()

class publish:

    client = paho.Client(paho.CallbackAPIVersion.VERSION1)

    def __init__(self):
        pass
    
    def encrypt_message(self, message):
        cipher_suite = Fernet(key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        payload = {
            "message": encrypted_message.decode(),  # Convert bytes to string
            "timestamp": datetime.now().isoformat()  # Add a timestamp to the payload
        }
        return json.dumps(payload)

    def on_publish(self, client, userdata, mid):
        print(str(mid) + " Sent from " + hostname)
        if userdata is not None:
            payload = json.loads(userdata)
            print("Latency time: " + str(payload["latency_time"]))

    def publish_loop(self, msg, topic):
        message = hostname + " sent: " + str(msg)
        try:
            encrypted_message = self.encrypt_message(message)
            (rc, mid) = self.client.publish('NAJ474/' + topic, encrypted_message, qos=1)
            # time.sleep(1)
        except Exception as e:
            print("An error occurred while encrypting or publishing the message:")
            print(str(e))
            # break
    
    def main_loop(self, msg, topic):
        self.client.on_publish = self.on_publish

        self.publish_loop(msg, topic)

        self.client.connect(the_broker)
        self.client.loop_start()

# client.loop_stop()
# client.disconnect()
