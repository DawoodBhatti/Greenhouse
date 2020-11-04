#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#script to activate the relay using GPIO pins 6, 13, 19, 26
def run_relay():
    # for GPIO numbering, choose BCM
    GPIO.setmode(GPIO.BCM)

    # or, for pin numbering, choose BOARD
    # GPIO.setmode(GPIO.BOARD)
    # but you can't have both, so only use one.

    GPIO.setup(6, GPIO.OUT)
    GPIO.output(6, GPIO.HIGH)

    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.HIGH)

    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.HIGH)

    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.HIGH)

    try:
        GPIO.output(26, GPIO.LOW)
        print("relay 1 on")
        time.sleep(3)

        GPIO.output(19, GPIO.LOW)
        print("relay 2 on")
        time.sleep(3)

        GPIO.output(13, GPIO.LOW)
        print("relay 3 on")
        time.sleep(3)

        GPIO.output(6, GPIO.LOW)
        print("relay 4 on")
        time.sleep(3)

        time.sleep(3)
        GPIO.cleanup()
        print("all off")

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("all off")
        print("quit")

    return None

run_relay()
