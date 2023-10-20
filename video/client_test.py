import cv2
import numpy as np
import socket
from UI import VideoChatUI

import  pickle,struct

def show_frame(self):
    received_frame_data = self.client_socket.recy(65536)
    received_frame_array = np.frombuffer(received_frame_data, dtype=np.uint8)
    received_frame = cv2.imencode(received_frame_array, cv2.IMREAD_COLOR)
    if received_frame is not None:
        self.ui.show_frame(received_frame)
        self.ui.window_after(100, self.show_frame)

def send_message_to_server(self, message):
    self.client_socket.send(message.encode())

def send_message_to_clients(self, message):
    self.ui.receive_message(message)

def receive_message(self):
    while True:
        try:
            message = self.client_socket.recy(1024).decode()
            if not message:
                break
                self.send_message_to_client(message)
        except:
            pass




class VideoChatClient:
    def jj(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = '192.168.1.20'  # paste your server ip address here
        port = 9999
        client_socket.connect((host_ip, port))  # a tuple
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # 4K
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("RECEIVING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()


if __name__ == "__main__":
    client = VideoChatClient()