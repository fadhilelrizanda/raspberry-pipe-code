import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--condition', type=bool, required=True)
args = parser.parse_args()

# GPIO pin connected to the servo
LAMP_PIN = 6

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LAMP_PIN, GPIO.OUT)

def turn_LED(condition):
    if condition:
        GPIO.output(LAMP_PIN,GPIO.HIGH)
        print("Turn On LED")
    else:
        GPIO.output(LAMP_PIN,GPIO.LOW)
        print("Turn Off LED")

    GPIO.cleanup()


if __name__=="__main__":
    turn_LED(args.condition)