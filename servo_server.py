import pigpio
import socket
import threading
import time

# Constants for pulse width and debounce
MIN_PULSE_WIDTH = 500  # Microseconds
MAX_PULSE_WIDTH = 2500  # Microseconds
debounce_delay = 0.6  # Debounce delay in seconds

# Setup GPIO using pigpio
servo_pin_1 = 12
servo_pin_2 = 13

# Connect to local pigpio daemon
pi = pigpio.pi()  # Connect to pigpio daemon

# Wait for the pigpio connection to be established
timeout = 10  # seconds
start_time = time.time()
while not pi.connected and (time.time() - start_time) < timeout:
    time.sleep(1)  # Wait a bit and try again

if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit(1)

print("Connected to pigpio daemon")

# Initialize PWM and set frequency
pi.set_mode(servo_pin_1, pigpio.OUTPUT)
pi.set_mode(servo_pin_2, pigpio.OUTPUT)
pi.set_PWM_frequency(servo_pin_1, 50)  # 50 Hz for servo control
pi.set_PWM_frequency(servo_pin_2, 50)  # 50 Hz for servo control

# Current angles, setting initial positions to 90 degrees
angle1 = 19  # Starting angle for servo 1
angle2 = 17  # Starting angle for servo 2

# Move servos to 90 degrees on startup
def set_servo_angle(pin, angle):
    pulsewidth = max(MIN_PULSE_WIDTH, min(MAX_PULSE_WIDTH, angle / 18 * 1000 + 500))
    pi.set_servo_pulsewidth(pin, pulsewidth)
    time.sleep(0.02)  # Wait for the servo to reach the position

# Set both servos to 90 degrees (normal condition) at startup
set_servo_angle(servo_pin_1, angle1)
set_servo_angle(servo_pin_2, angle2)
print("Servos initialized to 90 degrees")

def smooth_transition(pin, start_angle, end_angle, step=1, delay=0.01):
    if start_angle < end_angle:
        for angle in range(start_angle, end_angle + step, step):
            set_servo_angle(pin, angle)
            time.sleep(delay)
    else:
        for angle in range(start_angle, end_angle - step, -step):
            set_servo_angle(pin, angle)
            time.sleep(delay)

def handle_client_connection(client_socket):
    global angle1, angle2
    last_time = 0  # Initialize the last processed time
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            print(f"Received request: {request}")
            current_time = time.time()
            if current_time - last_time >= debounce_delay:
                if request == 'RIGHT' and angle1 > 5:
                    smooth_transition(servo_pin_1, angle1, angle1 - 1)
                    angle1 -= 1  # Decrease angle1
                elif request == 'LEFT' and angle1 < 35:
                    smooth_transition(servo_pin_1, angle1, angle1 + 1)
                    angle1 += 1  # Increase angle1
                elif request == 'UP' and angle2 > 0:
                    smooth_transition(servo_pin_2, angle2, angle2 - 1)
                    angle2 -= 1  # Decrease angle2
                elif request == 'DOWN' and angle2 < 25:
                    smooth_transition(servo_pin_2, angle2, angle2 + 1)
                    angle2 += 1  # Increase angle2
                last_time = current_time  # Update the last processed time
                print(f"Angle1: {angle1}, Angle2: {angle2}")
    except Exception as e:
        print(f"Error in client connection: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', 5000))
        server.listen(5)
        print("Server started on port 5000")
        while True:
            client_sock, addr = server.accept()
            print(f"Connection from {addr}")
            client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
            client_handler.start()
    except Exception as e:
        print(f"Error in starting server: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        pi.set_servo_pulsewidth(servo_pin_1, 0)
        pi.set_servo_pulsewidth(servo_pin_2, 0)
        pi.stop()
        print("Cleanup done")
