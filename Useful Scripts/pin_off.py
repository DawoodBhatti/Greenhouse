import RPi.GPIO as GPIO

# for GPIO numbering, choose BCM
GPIO.setmode(GPIO.BCM)

# or, for pin numbering, choose BOARD
# GPIO.setmode(GPIO.BOARD)
# but you can't have both, so only use one.
fan_pin = 26

GPIO.setup(fan_pin, GPIO.OUT)

GPIO.output(fan_pin, GPIO.LOW)
GPIO.cleanup()
