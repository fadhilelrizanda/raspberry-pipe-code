import argparse
from gpiozero import Servo

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--degree', type=int, required=True)
parser.add_argument('-s', '--servo', type=int, required=True)
args = parser.parse_args()

# GPIO pins connected to the servos
servo1 = Servo(12)
servo2 = Servo(13)

def convert_to_range(value, min_value=0, max_value=180, new_min=-1, new_max=1):
    # Check if the value is within the expected range
    if value < min_value or value > max_value:
        raise ValueError("Value out of range")
    
    # Perform the linear transformation
    new_value = ((value - min_value) * (new_max - new_min) / (max_value - min_value)) + new_min
    return new_value

def run_servo(servo_num, degree):
    angle_degrees = degree
    pulsewidth_micros = convert_to_range(angle_degrees)
    # Create PWM instance
    if servo_num == 1:
        servo1.value = pulsewidth_micros
        print(f"Servo 1 running at {pulsewidth_micros}")
    elif servo_num == 2:
        servo2.value = pulsewidth_micros
        print(f"Servo 2 running at {pulsewidth_micros}")
    else:
        print("Invalid servo number. Please specify 1 or 2.")

if __name__ == "__main__":
    run_servo(args.servo, args.degree)
