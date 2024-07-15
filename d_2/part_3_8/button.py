#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

class button:

    def __init__(self, button):
        GPIO.setmode(GPIO.BOARD)  # Setting the GPIO mode
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def on(self, button):
        while True:
            state = GPIO.input(button)
            time.sleep(0.3)

            if state == 0:
                return 1
            else:
                return 0
