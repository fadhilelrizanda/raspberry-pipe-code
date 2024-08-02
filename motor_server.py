import RPi.GPIO as GPIO
from pynput import keyboard
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

def on_press(key):
    try:
        if key.char == 'w':
            run_motor(1)  # Move forward when 'w' is pressed
        elif key.char == 's':
            run_motor(0)  # Move backward when 's' is pressed
    except AttributeError:
        pass

def on_release(key):
    motor_reset()  # Stop the motor when any key is released
    if key == keyboard.Key.esc:
        return False  # Stop listener

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
        # Start the keyboard listener in a separate thread
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        # Start the server
        start_server()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
