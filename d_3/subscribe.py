from cryptography.fernet import Fernet, InvalidToken
import paho.mqtt.client as paho
from datetime import datetime
import time
import json

import parking_1

print("\nSubscribing and ")

# Encryption key (should be the same as in publish.py)
key = "iHW-wSFTCFb1I2_7ZZWPfDpyP5ntoEVwWmltThQuaz8="

# the_broker = "broker.mqttdashboard.com"
# the_broker = "mqtt.eclipseprojects.io"
# the_broker = "test.mosquitto.org"
the_broker = "broker.emqx.io"

class subscribe:
    
    client = paho.Client(paho.CallbackAPIVersion.VERSION1)

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
        client.subscribe('NAJ474/parkings')

    def on_message(self, client, userdata, msg):
        global decrypted_message
        global new_temp
        global new_var
        # Decode the payload and parse it as JSON
        try:
            json_payload = json.loads(msg.payload.decode())
            # print("\n\033[91mReceived payload: ", json_payload)
            encrypted_message = json_payload['message']
            # print("\033[93mEncrypted message: " + encrypted_message)
            decrypted_message = self.decrypt_message(encrypted_message, key)
            
            if decrypted_message is not None:
                extracted_decrypted_message = decrypted_message.split(': ')[1]
            
            if extracted_decrypted_message == 'warning on':
                pass
            if extracted_decrypted_message == 'warning off':
                pass
            else:
                publish_time = datetime.fromisoformat(json_payload["timestamp"])
                latency = datetime.now() - publish_time

                # Extract temperature
                temp_str = extracted_decrypted_message.split(' C')[0]
                temp = round(float(temp_str), 3)  # Round to 3 decimal places

                # Extract spot number
                spot_str = extracted_decrypted_message.split('the spot ')[1]
                spot = int(spot_str.split(' is')[0])

                # Extract status
                status = extracted_decrypted_message.split(' is ')[1].rstrip('.')

                final_msg = f'Temperature: {temp}, Spot: {spot}, Status: {status}'
                # print(final_msg)

                # Temp to GUI
                self.new_var.temp_sensor_val.display(temp)

                # Parking spot status to GUI
                if spot == 16 and status == 'occupied':
                    self.new_var.parking_1.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                    "color: rgb(0,0,0);")
                if spot == 18 and status == 'occupied':
                    self.new_var.parking_2.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                    "color: rgb(0,0,0);")
                if spot == 22 and status == 'occupied':
                    self.new_var.parking_3.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                    "color: rgb(0,0,0);")
                if spot == 36 and status == 'occupied':
                    self.new_var.parking_4.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                    "color: rgb(0,0,0);")
                if spot == 38 and status == 'occupied':
                    self.new_var.parking_5.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                    "color: rgb(0,0,0);")

                
                if spot == 16 and status == 'empty':
                    self.new_var.parking_1.setStyleSheet("background-color: rgb(118, 118, 118);\n"
                    "color: rgb(255, 255, 255);")
                if spot == 18 and status == 'empty':
                    self.new_var.parking_2.setStyleSheet("background-color: rgb(118, 118, 118);\n"
                    "color: rgb(255, 255, 255);")
                if spot == 22 and status == 'empty':
                    self.new_var.parking_3.setStyleSheet("background-color: rgb(118, 118, 118);\n"
                    "color: rgb(255, 255, 255);")
                if spot == 36 and status == 'empty':
                    self.new_var.parking_4.setStyleSheet("background-color: rgb(118, 118, 118);\n"
                    "color: rgb(255, 255, 255);")
                if spot == 38 and status == 'empty':
                    self.new_var.parking_5.setStyleSheet("background-color: rgb(118, 118, 118);\n"
                    "color: rgb(255, 255, 255);")

                # print("Latency: ", latency.total_seconds() * 1000, "milliseconds\n")

        except json.JSONDecodeError:
            print("Invalid JSON payload")
        
        

    def main_loop(self, obj):
        # the_msg = decrypted_messag
        try:
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message

            self.new_var = obj
            # obj.temp_sensor_val.display(new_temp)

            self.client.connect(the_broker)
            self.client.loop_start()
            # time.sleep(1)

            # self.client.disconnect()
            # self.client.loop_stop()
            # return str(new_temp)
        except:
            pass

        # self.client.loop_forever()
        # print("the_msg: " + the_msg + "\n")

