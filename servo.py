#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) # this is really pin 11 on the pinout
p = GPIO.PWM(17, 50)
p.start(6)
input = sys.argv[1]


if (input == 'down'):
  print "moving down"
  p.ChangeDutyCycle(10.5) # up
  time.sleep(0.5)
elif (input == 'up'):
  print "moving up"
  p.ChangeDutyCycle(6.5) # down
  time.sleep(0.5)


# try:
  # while True:
    # p.ChangeDutyCycle(6) # up
    # time.sleep(5)
    # p.ChangeDutyCycle(2.2) # down
    # time.sleep(5)

# except KeyboardInterrupt:
  # p.stop()
  # GPIO.cleanup()

