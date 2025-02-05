import pioneer_sdk
import cv2
import socket
import pickle

camera = pioneer_sdk.Camera(timeout=2, video_buffer_size=250000, log_connection=False)

HOST = '127.0.0.1'
PORT = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting connection: ", HOST)
client_socket, addr = server_socket.accept()

while True:
    if client_socket:
        frame = camera.get_cv_frame()

        if frame is not None:
            print(type(frame))
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow("camera_server", frame)
        key = cv2.waitKey(1)

        if key == 27 or key == ord("q"):
            cv2.destroyAllWindows()
            client_socket.close()
            break