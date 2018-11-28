import socket
import threading
from Classes.TCPObserver import TCPObserver


class TCPThread(threading.Thread):
    ip = '0.0.0.0'
    port = 5006
    currentObservers = []

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

    def run(self):
        while 1:
            conn, addr = self.sock.accept()
            data = conn.recv(50000000)
            for observer in self.currentObservers:
                observer.notify(data)

    def subscribe(self, observer):
        print(isinstance(observer, TCPObserver))
        if isinstance(observer, TCPObserver):
            self.currentObservers.append(observer)
        else:
            raise Exception("Listener isn't from a TCPObserver")
