from config import connex_app
from config import SIM_CONTROLLER, USE_SIMULATION, SIM_REGISTER_FROM_DATABASE
from flask import render_template
from queue import Queue
from classes.TCPThread import TCPThread
from classes.HomeLynkController import HomeLynkController
from classes.simulation.devices.lamp import Lamp

connex_app.add_api('objects.yml')
"""Add the yml file to the api
"""


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
    HLController.daemon = True
    HLController.start()
    if USE_SIMULATION:
        SIM_CONTROLLER.set_queue(q)
        if SIM_REGISTER_FROM_DATABASE:
            SIM_CONTROLLER.register_devices_from_database()
        else:
            device = Lamp("Staande Lamp 01", '0/0/1')
            SIM_CONTROLLER.register_device(device)
        SIM_CONTROLLER.daemon = True
        SIM_CONTROLLER.start()


    else:
        socketThread = TCPThread(1, "Thread-1", 1, q)
        socketThread.subscribe(HLController)

        socketThread.daemon = True

        socketThread.start()

    connex_app.run(host='0.0.0.0', port=5001, debug=False)
