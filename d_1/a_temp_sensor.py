#!/usr/bin/env python3
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 13

class a_temp_sensor:

    def __init__(self):
        ADC.setup(0x48)  # Setting up the ADC module
        GPIO.setmode(GPIO.BOARD)  # Setting the GPIO mode
        GPIO.setup(DO, GPIO.IN)  # Setting up the digital output pin


    def Print(self, x):
        if x >= 20:
            return 'Hot'  # Return 'Hot' if the temperature is greater than or equal to 20
        elif x <= 20:
            return 'Cold'  # Return 'Cold' if the temperature is less than or equal to 20


    def loop(self):
        while True:
            analogVal = ADC.read(0)  # Reading the analog value from the ADC
            Vr = 5 * float(analogVal) / 255  # Calculating the voltage
            Rt = 10000 * Vr / (5 - Vr)  # Calculating the resistance
            temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))  # Calculating the temperature in Celsius
            temp = temp - 273.15  # Converting temperature to Celsius

            print ('temperature = ', temp, 'C')  # Printing the temperature in Celsius
            
            time.sleep(1)  # Delaying for 1 second

            return temp  # Returning the temperature

# if __name__ == '__main__':
#     try:
#         setup()
#         loop()
#     except KeyboardInterrupt:
#         pass
