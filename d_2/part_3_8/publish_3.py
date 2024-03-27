from cryptography.fernet import Fernet
import paho.mqtt.client as paho
from datetime import datetime
import socket
import time
import json
import os

os.system("clear")
print("Part 3: Publish")

# Generate a random encryption key
key = "iHW-wSFTCFb1I2_7ZZWPfDpyP5ntoEVwWmltThQuaz8="

# the_broker = "broker.mqttdashboard.com"
# the_broker = "mqtt.eclipseprojects.io"
# the_broker = "test.mosquitto.org"
the_broker = "broker.emqx.io"

hostname = socket.gethostname()

class publish_3:
    client = paho.Client()

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

    def publish_loop(self, x):
        # while True:
            # user_input = input("Give input here: ")

            # if user_input == "exit":
            #     message = hostname + " exited"
            #     encrypted_message = encrypt_message(message)
            #     (rc, mid) = client.publish('NAJ474/temp', encrypted_message, qos=1)
            #     break
            # else:
            # message = hostname + " sent: " + str(user_input)
            message = hostname + " sent: " + str(x)
            try:
                encrypted_message = self.encrypt_message(message)
                (rc, mid) = self.client.publish('NAJ474/temp', encrypted_message, qos=1)
                time.sleep(3)
            except Exception as e:
                print("An error occurred while encrypting or publishing the message:")
                print(str(e))
                # break
    
    def main_loop(self, x):
        # client = paho.Client()
        self.client.on_publish = self.on_publish

        self.publish_loop(x)

        self.client.connect(the_broker, 1883)
        self.client.loop_start()

# client.loop_stop()
# client.disconnect()
