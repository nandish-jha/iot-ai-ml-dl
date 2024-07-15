#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Defined some colors
white  = 0xffffff  # Hex code for white color
black  = 0x000000  # Hex code for black color
red    = 0xff0000  # Hex code for red color
orange = 0xff2200  # Hex code for orange color
yellow = 0xffff00  # Hex code for yellow color
green  = 0x00ff00  # Hex code for green color
cyan   = 0x00ddff  # Hex code for cyan color
blue   = 0x0000ff  # Hex code for blue color

colors = [red, orange, yellow, green, cyan, blue]  # List of colors

class rgb_led_module:
    
   def __init__(self, Rpin, Gpin, Bpin):
      global pins
      global p_R, p_G, p_B
      pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}  # Dictionary of pin numbers
      GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
      GPIO.setwarnings(False)
      
      for i in pins:
         GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
         GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to turn off led

      p_R = GPIO.PWM(pins['pin_R'], 2000)  # Set frequency to 2KHz
      p_G = GPIO.PWM(pins['pin_G'], 1999)
      p_B = GPIO.PWM(pins['pin_B'], 5000)

      p_R.start(100)      # Initial duty Cycle = 0 (leds off)
      p_G.start(100)
      p_B.start(100)

   def map(self, x, in_min, in_max, out_min, out_max):
      return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min  # Map a value from one range to another

   def off(self):
      GPIO.setmode(GPIO.BOARD)
      for i in pins:
         GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
         GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds

   def setColor(self, col):   # For example : col = 0x112233
      R_val = (col & 0xff0000) >> 16  # Extract the red value from the color
      G_val = (col & 0x00ff00) >> 8  # Extract the green value from the color
      B_val = (col & 0x0000ff) >> 0  # Extract the blue value from the color

      R_val = self.map(R_val, 0, 255, 0, 100)  # Map the red value to a duty cycle percentage
      G_val = self.map(G_val, 0, 255, 0, 100)  # Map the green value to a duty cycle percentage
      B_val = self.map(B_val, 0, 255, 0, 100)  # Map the blue value to a duty cycle percentage

      p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle of red LED
      p_G.ChangeDutyCycle(100-G_val)     # Change duty cycle of green LED
      p_B.ChangeDutyCycle(100-B_val)     # Change duty cycle of blue LED

   def loop(self):
      while True:
         for col in colors:
            self.setColor(col)  # Set the color
            time.sleep(1)  # Delay for 1 second

   def off(self):
      GPIO.setmode(GPIO.BOARD)
      for i in pins:
         GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
         GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds

   def destroy(self):
      p_R.stop()  # Stop PWM for red LED
      p_G.stop()  # Stop PWM for green LED
      p_B.stop()  # Stop PWM for blue LED
      self.off()  # Turn off all LEDs
      GPIO.cleanup()  # Clean up GPIO settings
   
   def power_on_loop(self):
      # Setting the color to cyan and waiting for 0.5 seconds
      self.setColor(yellow)
      time.sleep(0.5)

      # Setting the color to blue and waiting for 0.5 seconds
      self.setColor(black)
      time.sleep(0.5)

      # Setting the color to cyan and waiting for 0.5 seconds
      self.setColor(yellow)
      time.sleep(0.5)

      # Setting the color to blue and waiting for 0.5 seconds
      self.setColor(black)
      time.sleep(0.5)

      # Setting the color to cyan and waiting for 0.5 seconds
      self.setColor(yellow)
      # time.sleep(0.5)

# if __name__ == "__main__":
#    try:
#       setup(R, G, B)
#       loop()
#    except KeyboardInterrupt:
#       destroy()
