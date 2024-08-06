import argparse
import RPi.GPIO as GPIO
import time

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--degree', type=int, required=True, help="Desired angle for the servo (0-180)")
parser.add_argument('-s', '--servo', type=int, required=True, choices=[1, 2], help="Servo number (1 or 2)")
args = parser.parse_args()

# GPIO pins connected to the servos
Servo_pin1 = 12
Servo_pin2 = 13
GPIO.setmode(GPIO.BCM)  # Use board pin numbering
GPIO.setup(Servo_pin1, GPIO.OUT)
GPIO.setup(Servo_pin2, GPIO.OUT)

pwm1 = GPIO.PWM(Servo_pin1, 50)
pwm2 = GPIO.PWM(Servo_pin2, 50)

pwm1.start(0)
pwm2.start(0)

def set_angle(angle, servo_num, step=1, delay=0.02):
    if servo_num == 1:
        pwm = pwm1
    elif servo_num == 2:
        pwm = pwm2
    else:
        print("Invalid servo number. Please use 1 or 2.")
        return
    
    current_angle = 0
    for i in range(0, angle + 1, step):
        duty_cycle = 2 + (i / 18)
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(delay)

    time.sleep(1)
    pwm.ChangeDutyCycle(0)

if __name__ == "__main__":
    set_angle(args.degree, args.servo)
    GPIO.cleanup()  # Clean up GPIO on exit
