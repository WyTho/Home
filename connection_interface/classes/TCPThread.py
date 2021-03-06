import socket
import threading
from queue import Queue
from classes.TCPObserver import TCPObserver


class TCPThread(threading.Thread):
    """Thread for receiving TCP data from a Homelynk
    
    Arguments:
        threading {[Thread]} -- Thread implementation
    """
    ip = '0.0.0.0'
    port = 5006
    currentObservers = []
    text_color = "\033[1;32;40m "

    def __init__(self, threadID, name, counter, Q):
        """TCPThread initializer
        
        Arguments:
            threadID {[int]} -- Unique identifier for the thread
            name {[string]} -- Thread name
            counter {[int]} -- Thread counter
            Q {[Queue]} -- Shared data Queue
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        self.queue = Q

    def run(self):
        """Overrides threading.Thread.run()
        """
        while 1:
            conn, addr = self.sock.accept()
            data = conn.recv(50000000)
            self.queue.put(data)
            for observer in self.currentObservers:
                observer.notify(data)

    def subscribe(self, observer):
        """Subscribe method for observer pattern
        
        Arguments:
            observer {[TCPObserver]} -- Observer
        """
        if isinstance(observer, TCPObserver):
            self.currentObservers.append(observer)
        else:
            raise Exception("Listener isn't from a TCPObserver")
