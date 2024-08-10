import RPi.GPIO as GPIO
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

def run_motor(time_sleep, direction):
    print("Running Motor")
    if direction == 1:
        print("forward")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    elif direction == 2:
        print("Left")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
    elif direction == 3:
        print("Right")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    else:
        print("backward")
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    time.sleep(time_sleep)
    print(f"done {time_sleep} second(s)")
    motor_reset()

def handle_client_connection(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            if request == 'BACKWARD':
                run_motor(1, 1)
                
            elif request == 'FORWARD':
                run_motor(1, 0)
            elif request =="A":
                run_motor(1, 2)
            elif request =="D":
                run_motor(1, 3)
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
        start_server()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
