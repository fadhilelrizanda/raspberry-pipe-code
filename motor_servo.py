import RPi.GPIO as GPIO
import time
import argparse
from gpiozero import Servo

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--degree', type=int, required=True)
parser.add_argument('-s', '--servo', type=int, required=True)
args = parser.parse_args()

# GPIO pin connected to the servo

servo1 = Servo(12)
servo2 = Servo(13)


def map_value(angle, in_min, in_max, out_min, out_max):
    # Map 'angle' from the input range [in_min, in_max] to the output range [out_min, out_max]
    return int((angle - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def run_servo(servo_num, degree):
    angle_degrees = degree
    pulsewidth_micros = map_value(angle_degrees, 0, 180, -1, 1)
    # Create PWM instance
    if servo_num == 1:
        print(pulsewidth_micros)
        servo1.value(pulsewidth_micros)
        print(f"Servo 1 running {pulsewidth_micros}")
    else:
        print(pulsewidth_micros)
        servo2.value(pulsewidth_micros)
        print(f"Servo 2 running {pulsewidth_micros}")


if __name__ == "__main__":
    run_servo(args.servo,args.degree)
