from threading import Thread
import schedule
from classes.simulation.abstract.device import AbstractDevice
from classes.simulation.devices.lamp import Lamp
from models import Object
import json


class SimulationController(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.devices = []
        self.schedule = schedule
        self.queue = None

    def set_queue(self, Q):
        self.queue = Q

    def run(self):
        while True:
            self.schedule.run_pending()

    def handle_interact(self, address, new_value):
        obj = Object.query \
        .filter_by(address=address) \
        .first()

        for device in self.devices:
            if device.ADDRESS == obj.address:
                current_obj = {"address": device.ADDRESS,
                               "id": obj.id,
                               "value": new_value}
                self.queue.put(json.dumps(current_obj))

    def register_device(self, device):
        if isinstance(device, AbstractDevice):
            self.devices.append(device)
            if device.DO_MAIN_LOOP:
                self.schedule.every(device.MAIN_LOOP_SCHEDULE).seconds.do(device.main_loop())
        else:
            raise TypeError('Object is not a derivative of AbstractDevice')

    def register_devices_from_database(self):
        objects = Object.query \
        .filter(Object.script_id.isnot(None)) \
        .all()

        for object in objects:
            if(object.script_id == 1):
                device = Lamp(object.name, object.address)
                self.register_device(device)

