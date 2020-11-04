import RPi.GPIO as GPIO

# for GPIO numbering, choose BCM
GPIO.setmode(GPIO.BCM)

# or, for pin numbering, choose BOARD
# GPIO.setmode(GPIO.BOARD)
# but you can't have both, so only use one.

GPIO.setup(21, GPIO.OUT)

GPIO.output(21, GPIO.LOW)
GPIO.cleanup()
