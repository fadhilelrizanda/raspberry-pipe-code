import RPi.GPIO as GPIO
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t','--time_sleep',type=int,required=True)
parser.add_argument('-d','--direction',type=int,required=True)
args= parser.parse_args()

# Define pinout
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)

def run_motor(time_sleep,direction):
    print("Running Motor")
    if direction == 1:
        print("forward")
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.HIGH)
    else:
        print("backward")
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.HIGH)
        GPIO.output(IN4,GPIO.LOW)
    time.sleep(time_sleep)
    print(f"done {time_sleep} second s")
    GPIO.cleanup()


if __name__ == "__main__":
    run_motor(args.time_sleep,args.direction)