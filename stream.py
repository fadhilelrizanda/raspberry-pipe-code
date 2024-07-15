import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import socket
import cv2
import struct
import pickle
import threading
import picommand

host_name = "robot.local"
port = 22
username = "robot"
password = "robot12345678"

# Create the main window
window = tk.Tk()

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size and title
window.geometry("%dx%d" % (screen_width, screen_height))
window.title("Robot Pipeline Inspection V1")

# Create a blank image for default size
frame_width, frame_height = 800, 400
default_image = Image.new('RGBA', (frame_width, frame_height), (255, 255, 255, 255))
default_photo_image = ImageTk.PhotoImage(default_image)

# Flag to control streaming
streaming = False

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.1.100"  # Replace with your Raspberry Pi's IP address
port = 9999

# Connect to the server
try:
    client_socket.connect((host_ip, port))
    log_console(f"Connected to server at {host_ip}:{port}")
except ConnectionRefusedError:
    log_console(f"Connection refused at {host_ip}:{port}")
    client_socket.close()

data = b""
payload_size = struct.calcsize("Q")

def start_stream():
    global streaming
    streaming = True
    log_console("Starting stream...")
    stream_video()

def stream_video():
    global data
    if streaming:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                return
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        image_video.imgtk = imgtk
        image_video.configure(image=imgtk)
        image_video.after(10, stream_video)

def stop_stream():
    global streaming
    streaming = False
    client_socket.close()
    image_video.configure(image=default_photo_image)
    log_console("Stopped stream. Exiting...")
    window.destroy()

def log_console(message):
    console_text.configure(state='normal')
    console_text.insert(tk.END, message + '\n')
    console_text.configure(state='disabled')
    console_text.yview(tk.END)

def run_motor():
    check_val = motor_scale.get()
    if check_val > 0:
        dir_code = 0
        log_console(f"Run Motor forward {check_val}")
    else:
        dir_code = 1
        log_console(f"Run Motor backward {check_val}")

    command = f"python /home/robot/code/pipeline-robot-code/motor.py --time {abs(check_val)} --d {dir_code}"
    picommand.ssh_command(host_name, port, username, password, command)

def run_motor_left_right():
    degree_servo = camera_left_right_scale.get()
    servo_code = 1
    if degree_servo < 0:
        log_console(f"Run servo left {degree_servo} code {servo_code}")

    else:
        log_console(f"Run servo right {degree_servo} code {servo_code}")

    command = f"python /home/robot/code/pipeline-robot-code/motor_servo.py --d {abs(degree_servo)} --s {servo_code}"
    picommand.ssh_command(host_name, port, username, password, command)

def run_motor_up_down():
    degree_servo = camera_up_down
