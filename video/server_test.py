import time

import cv2
from socket import *
import threading
from UI import VideoChatUI
import tkinter as tk
import imutils, pickle,struct

class VideoChatServer:
    def __init__(self):
        self.ul = VideoChatUI(tk.TK(), "화상 채팅 시작")
        self.ul.on_send_message = self.send_message_to_clients
        self.clients = []

        #설정 초기화
        self.cap = cv2.VideoCapture(0)

        #소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        port = 9999
        socket_address = (host_ip, port)
        self.server_socket.bind(socket_address)
        self.server_socket.listen(5)
        print("대기",socket_address )

        #웹캠 영산 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        #클라이언트 연결을 처리하는 스레드 시작

        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        #서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        for client in self.client:
            client.send(message.encode())
        #서버 ui에도 메세지 표시
        self.ui.receive_message("서버: "+message)

    def send_message_to_server(self, message):
        self.ui.receive_message(message)
        self.send_message_to_clients(message)

    def update(self):

        while True:
            if self.started:
                (grabbed, frame) = self.capture.read()

                if grabbed:
                    self.Q.put(frame)

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
                encode_frame= cv2.imencode( '.jpg', frame,[int(cv2.IMWRITE_JPEG_QUALITY), 60])
                encode_frame = encode_frame.tobytes()
                for client in self.client:
                    try:
                        client.send(encode_frame)
                    except:
                        self.client_remove(client)

                #서버 ui에도 비디오화면 표시
                self.show_frame(frame)

    def fps(self):

        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time

        if self.sec > 0:
            fps = round(1 / (self.sec), 1)

        else:
            fps = 1

        return fps

    def accept(self):
        # Socket Accept
        while True:
            client_socket, addr = self.server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if client_socket:
                vid = cv2.VideoCapture(0)

                while (vid.isOpened()):
                    img, frame = vid.read()
                    frame = imutils.resize(frame, width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

                    cv2.imshow('TRANSMITTING VIDEO', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        client_socket.close()
        close()