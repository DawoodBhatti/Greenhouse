#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#script to activate the 4-channel relay using GPIO pins
def run_relay(run_time=1200):
    # for GPIO numbering, choose BCM
    GPIO.setmode(GPIO.BCM)

    # or, for pin numbering, choose BOARD
    # GPIO.setmode(GPIO.BOARD)
    # but you can't have both, so only use one.

    #using GPIO pin 13 to activate LED
    #GPIO.setup(13, GPIO.OUT)
    #GPIO.output(13, GPIO.HIGH)

    #using GPIO pin 19 to active humidifier
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.HIGH)

    #using GPIO pin 26 to activate fans
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.HIGH)


    try:
        GPIO.output(26, GPIO.LOW)
        print("relay 1 on")

        GPIO.output(19, GPIO.LOW)
        print("relay 3 on")
        time.sleep(run_time)

        GPIO.cleanup()
        print("all off")

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("all off")
        print("quit")

    return None

#run_relay()
