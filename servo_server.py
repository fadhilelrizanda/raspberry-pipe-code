import pigpio
import socket
import threading
import time
import subprocess

# Check if pigpiod is running
def check_pigpiod():
    try:
        subprocess.run(['pgrep', 'pigpiod'], check=True, stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# Start the pigpiod daemon
def start_pigpiod():
    try:
        subprocess.run(['sudo', 'pigpiod'], check=True)
        print("pigpiod started successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start pigpiod: {e}")

# Stop the pigpiod daemon
def stop_pigpiod():
    try:
        subprocess.run(['sudo', 'pkill', 'pigpiod'], check=True)
        print("pigpiod stopped successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop pigpiod: {e}")

# Setup GPIO using pigpio
servo_pin_1 = 12
servo_pin_2 = 13

# Ensure pigpiod is running
if not check_pigpiod():
    start_pigpiod()
    time.sleep(5)  # Wait for pigpiod to initialize

pi = pigpio.pi()  # Connect to local pigpio daemon

# Wait for the pigpio connection to be established
timeout = 10  # seconds
start_time = time.time()
while not pi.connected and (time.time() - start_time) < timeout:
    time.sleep(1)  # Wait a bit and try again

if not pi.connected:
    print("Failed to connect to pigpio daemon")
    stop_pigpiod()
    exit(1)

print("Connected to pigpio daemon")

# Initialize PWM
pi.set_mode(servo_pin_1, pigpio.OUTPUT)
pi.set_mode(servo_pin_2, pigpio.OUTPUT)

# Current angles
angle1 = 90  # Starting angle for servo 1
angle2 = 90  # Starting angle for servo 2

# Debounce delay in seconds
debounce_delay = 0.2  # Adjust this value as needed

def set_servo_angle(pin, angle):
    pulsewidth = angle / 18 + 500  # Convert angle to pulsewidth
    pi.set_servo_pulsewidth(pin, pulsewidth)
    time.sleep(0.02)  # Wait for the servo to reach the position
    time.sleep(3)  # hold
    pi.set_servo_pulsewidth(pin, 0)  # Stop sending the signal

def handle_client_connection(client_socket):
    global angle1, angle2
    last_time = 0  # Initialize the last processed time
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            current_time = time.time()
            if current_time - last_time >= debounce_delay:
                if request == 'LEFT':
                    angle1 = max(0, angle1 - 5)  # Decrease angle1
                    set_servo_angle(servo_pin_1, angle1)
                elif request == 'RIGHT':
                    angle1 = min(180, angle1 + 5)  # Increase angle1
                    set_servo_angle(servo_pin_1, angle1)
                elif request == 'UP':
                    angle2 = max(0, angle2 - 5)  # Decrease angle2
                    set_servo_angle(servo_pin_2, angle2)
                elif request == 'DOWN':
                    angle2 = min(180, angle2 + 5)  # Increase angle2
                    set_servo_angle(servo_pin_2, angle2)
                last_time = current_time  # Update the last processed time
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
        # Stop pigpiod and clean up
        stop_pigpiod()
        pi.set_servo_pulsewidth(servo_pin_1, 0)
        pi.set_servo_pulsewidth(servo_pin_2, 0)
        pi.stop()
        print("Cleanup done")
