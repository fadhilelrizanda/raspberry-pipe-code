import RPi.GPIO as GPIO
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--degree', type=int, required=True)
parser.add_argument('-s', '--servo', type=int, required=True)
args = parser.parse_args()

# GPIO pin connected to the servo
SERVO_PIN = [13,12]

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)

def map_value(angle, in_min, in_max, out_min, out_max):
    # Map 'angle' from the input range [in_min, in_max] to the output range [out_min, out_max]
    return int((angle - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def run_servo(servo_num, degree):
    angle_degrees = degree
    pulsewidth_micros = map_value(angle_degrees, 0, 180, 1000, 2000)
    # Create PWM instance
    servo = GPIO.PWM(SERVO_PIN[servo_num], 50)  # 50 Hz frequency


        # Start PWM
    # servo.start(0)  # Start with 0% duty cycle
        
        # Move the servo to the desired degree position
    servo.ChangeDutyCycle(5 + (pulsewidth_micros - 1000) / 10)  # Convert microseconds to duty cycle
        
    time.sleep(1)
    
    servo.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")
    print(f"Servo {servo_num} degree{degree} pwm{pulsewidth_micros}")

if __name__ == "__main__":
    run_servo(args.servo,args.degree)
