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

def smooth_servo_angle(pwm, current_angle, target_angle, step=1, delay=0.02):
    if current_angle < target_angle:
        for angle in range(current_angle, target_angle + 1, step):
            duty = angle / 18 + 2
            pwm.ChangeDutyCycle(duty)
            time.sleep(delay)
    elif current_angle > target_angle:
        for angle in range(current_angle, target_angle - 1, -step):
            duty = angle / 18 + 2
            pwm.ChangeDutyCycle(duty)
            time.sleep(delay)
    # Hold the final position
    final_duty = target_angle / 18 + 2
    pwm.ChangeDutyCycle(final_duty)
    time.sleep(2)
    pwm.ChangeDutyCycle(0)  # Stop sending the signal

def handle_client_connection(client_socket):
    global angle1, angle2
    last_command_time = time.time()
    debounce_time = 0.2  # 200ms debounce time
    
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            
            current_time = time.time()
            if current_time - last_command_time < debounce_time:
                continue  # Skip this command if it's within the debounce period
            
            last_command_time = current_time  # Update last command time
            
            if request == 'LEFT':
                new_angle1 = max(0, angle1 - 5)  # Decrease angle1
                smooth_servo_angle(pwm1, angle1, new_angle1)
                angle1 = new_angle1
            elif request == 'RIGHT':
                new_angle1 = min(180, angle1 + 5)  # Increase angle1
                smooth_servo_angle(pwm1, angle1, new_angle1)
                angle1 = new_angle1
            elif request == 'UP':
                new_angle2 = max(0, angle2 - 5)  # Decrease angle2
                smooth_servo_angle(pwm2, angle2, new_angle2)
                angle2 = new_angle2
            elif request == 'DOWN':
                new_angle2 = min(180, angle2 + 5)  # Increase angle2
                smooth_servo_angle(pwm2, angle2, new_angle2)
                angle2 = new_angle2
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
