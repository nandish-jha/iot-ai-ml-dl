from cryptography.fernet import Fernet, InvalidToken
import paho.mqtt.client as paho
from datetime import datetime
import json
import os

os.system("clear")
print("Part 2: Subscribe")

# Encryption key (should be the same as in publish.py)
key = "iHW-wSFTCFb1I2_7ZZWPfDpyP5ntoEVwWmltThQuaz8="

# the_broker = "broker.mqttdashboard.com"
# the_broker = "mqtt.eclipseprojects.io"
# the_broker = "test.mosquitto.org"
the_broker = "broker.emqx.io"

def decrypt_message(encrypted_message, key):
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

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('messages/#')

def on_message(client, userdata, msg):
    # Decode the payload and parse it as JSON
    try:
        json_payload = json.loads(msg.payload.decode())
        print("\n\033[91mReceived payload: ", json_payload)
        
        encrypted_message = json_payload['message']
        print("\033[93mEncrypted message: " + encrypted_message)
        
        decrypted_message = decrypt_message(encrypted_message, key)
        
        if decrypted_message is not None:
            print("\033[1;4;92mDecrypted message " + decrypted_message + "\033[0m")
            
            # Calculate the latency
            publish_time = datetime.fromisoformat(json_payload["timestamp"])
            latency = datetime.now() - publish_time
            print("Latency: ", latency.total_seconds() * 1000, "milliseconds\n")

    except json.JSONDecodeError:
        print("Invalid JSON payload")

client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(the_broker, 1883)
client.loop_forever()
