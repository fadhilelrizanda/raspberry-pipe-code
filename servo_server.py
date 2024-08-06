import RPi.GPIO as GPIO
import socket
import threading
import time

# Setup GPIO
servo_pin_1 = 12
servo_pin_2 = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_1, GPIO.OUT)
GPIO.setup(servo_pin_2, GPIO.OUT)

# Initialize PWM
pwm1 = GPIO.PWM(servo_pin_1, 50)
pwm2 = GPIO.PWM(servo_pin_2, 50)
pwm1.start(0)
pwm2.start(0)

# Current angles
angle1 = 90  # Starting angle for servo 1
angle2 = 90  # Starting angle for servo 2

def set_servo_angle(pwm, angle):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.02)  # Wait for the servo to reach the position
    time.sleep(2)
    pwm.ChangeDutyCycle(0)  # Stop sending the signal

def handle_client_connection(client_socket):
    global angle1, angle2
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            if request == 'LEFT':
                angle1 = max(0, angle1 - 5)  # Decrease angle1
                set_servo_angle(pwm1, angle1)
            elif request == 'RIGHT':
                angle1 = min(180, angle1 + 5)  # Increase angle1
                set_servo_angle(pwm1, angle1)
            elif request == 'UP':
                angle2 = max(0, angle2 - 5)  # Decrease angle2
                set_servo_angle(pwm2, angle2)
            elif request == 'DOWN':
                angle2 = min(180, angle2 + 5)  # Increase angle2
                set_servo_angle(pwm2, angle2)
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Server started on port 5000")
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
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()
