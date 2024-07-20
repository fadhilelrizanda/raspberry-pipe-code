import argparse
import RPi.GPIO as GPIO
import time

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--degree', type=int, required=True)
parser.add_argument('-s', '--servo', type=int, required=True)
args = parser.parse_args()

# GPIO pins connected to the servos
Servo_pin1 = 12
Servo_pin2 = 13
GPIO.setup(Servo_pin1,GPIO.out)
GPIO.setup(Servo_pin2,GPIO.out)

pwm = GPIO.PWM(Servo_pin1,50)
pwm2 = GPIO.PWM(Servo_pin2,50)

pwm1.start(0)
pwm2.start(0)

def set_angle(angle,servo_num):
    duty_cycle = (angle/18)+2
    if servo_num==1:
        GPIO.output(Servo_pin1,True)
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)  # Wait for the servo to reach the angle

    else:
        GPIO.output(servo_pin, False)
        pwm.ChangeDutyCycle(0)
        time.sleep(1)
    print(f"Run Servo {servo_num} {angle} {duty_cycle}")

if __name__ == "__main__":
    set_angle(args.degree, args.servo)

    