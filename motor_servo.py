import argparse
import RPi.GPIO as GPIO
import time


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--degree', type=int, required=True, help="Desired angle for the servo (0-180)")
parser.add_argument('-s', '--servo', type=int, required=True, choices=[1, 2], help="Servo number (1 or 2)")
args = parser.parse_args()

# GPIO pins connected to the servos pin 12 and 13
Servo_pin1 = 12
Servo_pin2 = 13
GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
GPIO.setup(Servo_pin1, GPIO.OUT)
GPIO.setup(Servo_pin2, GPIO.OUT)

pwm = GPIO.PWM(Servo_pin1, 50)
pwm2 = GPIO.PWM(Servo_pin2, 50)

pwm.start(0)
pwm2.start(0)

def set_angle(angle, servo_num):
    if servo_num == 1:
        pwm.ChangeDutyCycle(2 + (angle / 18))  # Calculate duty cycle for Servo 1
        time.sleep(1)  # Wait for the servo to reach the angle
        pwm.ChangeDutyCycle(0)  # Stop sending PWM signal
    elif servo_num == 2:
        pwm2.ChangeDutyCycle(2 + (angle / 18))  # Calculate duty cycle for Servo 2
        time.sleep(1)  # Wait for the servo to reach the angle
        pwm2.ChangeDutyCycle(0)  # Stop sending PWM signal
    else:
        print("Invalid servo number. Please use 1 or 2.")

if __name__ == "__main__":
    set_angle(args.degree, args.servo)
    GPIO.cleanup()  # Clean up GPIO on exit
