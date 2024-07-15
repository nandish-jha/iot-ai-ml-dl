from rgb_led_module import rgb_led_module  # Importing the RGB LED module
from a_temp_sensor  import a_temp_sensor   # Importing the temperature sensor module
from button         import button          # Importing the button module
import time

# import paho.mqtt.client as paho

from publish_3 import publish_3

# the_broker = "broker.emqx.io"
# client = paho.Client()
# client.connect(the_broker)
# client.loop_start()

power = 0  # Variable to store the state of the button

# PIN numbers for the button and the LEDs
X = 37  # Pin number for the button
R = 29  # Pin number for the red LED
G = 31  # Pin number for the green LED
B = 33  # Pin number for the blue LED

# Defined some colors
white  = 0xffffff  # Hex code for white color
black  = 0x000000  # Hex code for black color
red    = 0xff0000  # Hex code for red color
orange = 0xff2200  # Hex code for orange color
yellow = 0xffff00  # Hex code for yellow color
green  = 0x00ff00  # Hex code for green color
cyan   = 0x00ddff  # Hex code for cyan color
blue   = 0x0000ff  # Hex code for blue color

# class object instantiations
rgb_inst_1 = rgb_led_module(R, G, B) # Creating an instance of the RGB LED module
temp_inst_1 = a_temp_sensor() # Creating an instance of the temperature sensor module
button_inst_1 = button(X) # Creating an instance of the button module

publish_inst_1 = publish_3()

rgb_inst_1.power_on_loop()

while True:
    try:
    #     if button_inst_1.on(X) == 1:
    #         power = True
        
        # while power is True:
        current_temperature = temp_inst_1.loop()
        publish_inst_1.main_loop(current_temperature)
        hc_flag = temp_inst_1.Print(current_temperature)
        
        if hc_flag == 'Hot':
            rgb_inst_1.setColor(orange)  # Setting the color to orange if the temperature is hot
        elif hc_flag == 'Cold':
            rgb_inst_1.setColor(cyan)  # Setting the color to cyan if the temperature is coldEDs
            
            # if button_inst_1.on(X) == 0:
            #     power = False
            #     break
    except KeyboardInterrupt:
        rgb_inst_1.destroy()
        break
