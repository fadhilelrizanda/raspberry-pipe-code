import RPi.GPIO as GPIO
import keyboard
import socket
import threading
import time

# Define pinout
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 16

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def motor_reset():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def run_motor(direction):
    print("Running Motor")
    if direction == 1:
        print("forward")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    else:
        print("backward")
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)

def handle_key_event():
    while True:
        if keyboard.is_pressed('w'):
            run_motor(1)  # Move forward when 'w' is pressed
        elif keyboard.is_pressed('s'):
            run_motor(0)  # Move backward when 's' is pressed
        else:
            motor_reset()  # Stop the motor when no key is pressed
        time.sleep(0.1)  # Sleep to prevent high CPU usage

def handle_client_connection(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                motor_reset()
                break
            if request == 'FORWARD':
                run_motor(1)
            elif request == 'BACKWARD':
                run_motor(0)
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5050))
    server.listen(5)
    print("Motor Server started on port 5050")
    while True:
        client_sock, addr = server.accept()
        client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    try:
        # Start the keyboard event handler thread
        keyboard_thread = threading.Thread(target=handle_key_event)
        keyboard_thread.daemon = True
        keyboard_thread.start()

        # Start the server
        start_server()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
