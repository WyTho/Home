from config import connex_app
from flask import render_template
from queue import Queue
from classes.TCPObserver import TCPObserver
from classes.TCPThread import TCPThread
from classes.HomeLynkController import HomeLynkController

# Read the objects.yml file to configure the endpoints
connex_app.add_api('objects.yml')


# Create a URL route in our application for "/"
@connex_app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'index.html'
    """
    return render_template('index.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    q = Queue()
    HLController = HomeLynkController(q)
    socketThread = TCPThread(1, "Thread-1", 1, q)
    socketThread.subscribe(HLController)

    socketThread.daemon = True
    HomeLynkController.deamon = True

    socketThread.start()
    HLController.start()
    connex_app.run(host='0.0.0.0', port=5000, debug=True)
