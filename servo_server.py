import pigpio
import socket
import threading
import time

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

# Initialize PWM
pi.set_mode(servo_pin_1, pigpio.OUTPUT)
pi.set_mode(servo_pin_2, pigpio.OUTPUT)

# Current angles
angle1 = 90  # Starting angle for servo 1
angle2 = 90  # Starting angle for servo 2

# Debounce delay in seconds
debounce_delay = 0.2  # Adjust this value as needed

def set_servo_angle(pin, angle):
    pulsewidth = max(500, min(2500, angle / 18 * 1000 + 500))  # Convert angle to pulsewidth within valid range
    pi.set_servo_pulsewidth(pin, pulsewidth)
    time.sleep(0.02)  # Wait for the servo to reach the position
    # time.sleep(3)  # hold
    # pi.set_servo_pulsewidth(pin, 0)  # Stop sending the signal

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
                if request == 'RIGHT':
                    angle1 = max(5, angle1 - 2)  # Decrease angle1
                    set_servo_angle(servo_pin_1, angle1)
                elif request == 'LEFT':
                    angle1 = min(35, angle1 + 2)  # Increase angle1
                    set_servo_angle(servo_pin_1, angle1)
                elif request == 'UP':
                    angle2 = max(0, angle2 - 2)  # Decrease angle2
                    set_servo_angle(servo_pin_2, angle2)
                elif request == 'DOWN':
                    angle2 = min(180, angle2 + 2)  # Increase angle2
                    set_servo_angle(servo_pin_2, angle2)
                last_time = current_time  # Update the last processed time
                print(angle1)
                print(angle2)
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
