import socket
import cv2
import struct
import pickle

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '0.0.0.0'  # Listen on all available interfaces
port = 9999
socket_address = (host_ip, port)

# Bind and listen
server_socket.bind(socket_address)
server_socket.listen(5)
print("Listening at:", socket_address)

# Accept a connection
client_socket, addr = server_socket.accept()
print('Connection from:', addr)

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    message_size = struct.pack("Q", len(data))
    try:
        client_socket.sendall(message_size + data)
    except:
        break

cap.release()
client_socket.close()
server_socket.close()
