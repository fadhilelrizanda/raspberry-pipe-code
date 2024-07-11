import pigpio
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d','--degree',type=int,required=True)

args= parser.parse_args()

# GPIO pin connected to the servo
SERVO_PIN = 17

# Initialize pigpio
pi = pigpio.pi()

def map_value(angle, in_min, in_max, out_min, out_max):
    # Map 'angle' from the input range [in_min, in_max] to the output range [out_min, out_max]
    return int((angle - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)



def run_servo(degree):

    try:
        angle_degrees = degree  # Example angle in degrees
        pulsewidth_micros = map_value(angle_degrees, 0, 180, 1000, 2000)
        # Start PWM on the servo pin
        pi.set_mode(SERVO_PIN, pigpio.OUTPUT)
        pi.set_servo_pulsewidth(SERVO_PIN, 0)  # Start with 0% duty cycle
        
     
        # Move the servo to the 0 degree position
        pi.set_servo_pulsewidth(SERVO_PIN, pulsewidth_micros)  # Move to 0 degree position
        time.sleep(1)
        print(f"Servo move {degree}, pwm {pulsewidth_micros}")
        


    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Cleaning up and exiting...")

    finally:
        # Clean up
        pi.set_servo_pulsewidth(SERVO_PIN, 0)  # Stop PWM
        pi.stop()
        print("GPIO cleanup complete.")


if __name__ == "__main__":
    run_servo(args.degree)
