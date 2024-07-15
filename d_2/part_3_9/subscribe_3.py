from cryptography.fernet import Fernet, InvalidToken
import paho.mqtt.client as paho
from datetime import datetime
import time
import json
import os

os.system("clear")
print("Part 3: Subscribe")

# Encryption key (should be the same as in publish.py)
key = "iHW-wSFTCFb1I2_7ZZWPfDpyP5ntoEVwWmltThQuaz8="

# the_broker = "broker.mqttdashboard.com"
# the_broker = "mqtt.eclipseprojects.io"
# the_broker = "test.mosquitto.org"
the_broker = "broker.emqx.io"

# global decrypted_message 

class subscribe_3:
    
    client = paho.Client()
    def __init__(self):
        pass
    
    def decrypt_message(self, encrypted_message, key):
        try:
            cipher_suite = Fernet(key)
            
            # Check if the input is a bytes-like object
            if isinstance(encrypted_message, str):
                encrypted_message = encrypted_message.encode()
            
            # Add padding characters if needed
            padding = b'=' * (4 - (len(encrypted_message) % 4))
            encrypted_message += padding
            
            decrypted_message = cipher_suite.decrypt(encrypted_message)
            return decrypted_message.decode()
        except InvalidToken:
            print("Invalid token. Unable to decrypt the message.")
            return None

    def on_connect(self, client, userdata, flags, rc):
        # print("Connected with result code " + str(rc))
        client.subscribe('NAJ474/#')

    def on_message(self, client, userdata, msg):
        global decrypted_message
        # Decode the payload and parse it as JSON
        try:
            json_payload = json.loads(msg.payload.decode())
            # print("\n\033[91mReceived payload: ", json_payload)
            encrypted_message = json_payload['message']
            # print("\033[93mEncrypted message: " + encrypted_message)
            decrypted_message = self.decrypt_message(encrypted_message, key)
            
            if decrypted_message is not None:
                print("\nReceived\n" + decrypted_message)
                
                # Calculate the latency
                publish_time = datetime.fromisoformat(json_payload["timestamp"])
                latency = datetime.now() - publish_time
                print("Latency: ", latency.total_seconds() * 1000, "milliseconds\n")

        except json.JSONDecodeError:
            print("Invalid JSON payload")
        
        

    def main_loop(self):
        # the_msg = decrypted_messag
        try:
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message

            self.client.connect(the_broker, 1883)
            self.client.loop_start()
            time.sleep(3)
            self.client.disconnect()
            self.client.loop_stop()
            return decrypted_message
        except:
            pass

        # self.client.loop_forever()
        # print("the_msg: " + the_msg + "\n")

