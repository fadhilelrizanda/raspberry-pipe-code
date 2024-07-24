import socket
import struct
import time
from picamera2 import Picamera2
from io import BytesIO

# Function to capture frames and send over the network
def stream_camera(connection):
    camera = Picamera2()
    camera_config = camera.create_still_configuration(main={"size": (640, 480)})
    camera.configure(camera_config)
    camera.start()

    stream = BytesIO()

    try:
        while True:
            stream.seek(0)
            camera.capture_file(stream, format="jpeg")
            image_data = stream.getvalue()

            # Send the size of the image
            connection.write(struct.pack('<L', len(image_data)))
            connection.flush()

            # Send the image data
            connection.write(image_data)
            connection.flush()

            # Add a small delay to simulate video frame rate
            time.sleep(0.05)
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        camera.stop()
        connection.close()
        print("Connection closed")

# Set up the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8080))  # Changed port to 8080
    server_socket.listen(0)
    server_socket.settimeout(10)  # Set a timeout for accepting connections
    print("Server started, waiting for connections...")

    try:
        while True:
            try:
                connection = server_socket.accept()[0].makefile('wb')
                print("Client connected")
                stream_camera(connection)
            except socket.timeout:
                print("Server accept timeout, no connections received.")
                continue
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server_socket.close()
        print("Server closed")

if __name__ == "__main__":
    start_server()
