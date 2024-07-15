import socket
import cv2
import pickle
import struct
import subprocess
import numpy as np

def capture_frame():
    # Capture a single frame using libcamera
    command = ["libcamera-still", "-o", "-", "--width", "640", "--height", "480", "--nopreview"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode == 0:
        # Convert the captured frame to a numpy array
        frame = np.frombuffer(out, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        return frame
    else:
        print(f"Error capturing frame: {err}")
        return None

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.200.2'  # Replace with your Raspberry Pi's IP address
    port = 9999

    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(5)
    print(f"Listening on {socket_address}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        if client_socket:
            while True:
                frame = capture_frame()
                if frame is None:
                    print("Failed to capture frame")
                    break

                # Encode frame to JPEG format
                encoded, buffer = cv2.imencode('.jpg', frame)
                if not encoded:
                    print("Failed to encode frame")
                    continue

                a = pickle.dumps(buffer)
                message = struct.pack("Q", len(a)) + a
                try:
                    client_socket.sendall(message)
                except Exception as e:
                    print(f"Error sending frame: {e}")
                    break

            client_socket.close()

if __name__ == "__main__":
    main()
