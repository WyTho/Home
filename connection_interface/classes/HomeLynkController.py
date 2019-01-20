from classes.TCPObserver import TCPObserver
import threading


class HomeLynkController(threading.Thread, TCPObserver):
    text_color = "\033[1;31;40m "

    def __init__(self, Q):
        self.queue = Q
        threading.Thread.__init__(self)

    def check_type(self, data):
        return data

    def handle_data(self, data):
        print(self.text_color + data.decode("utf-8"))
        return True

    def run(self):
        while True:
            data = self.queue.get()
            self.handle_data(data)

    def notify(self, data):
        return

