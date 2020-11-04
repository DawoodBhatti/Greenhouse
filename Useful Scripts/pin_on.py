import RPi.GPIO as GPIO

# for GPIO numbering, choose BCM
GPIO.setmode(GPIO.BCM)

# or, for pin numbering, choose BOARD
# GPIO.setmode(GPIO.BOARD)
# but you can't have both, so only use one.
heater_pin = 21

GPIO.setup(heater_pin,GPIO.OUT)

GPIO.output(heater_pin,GPIO.HIGH)

