from threading import Thread
import time
import schedule
from classes.simulation.abstract.device import AbstractDevice
from classes.simulation.devices.lamp import Lamp
from classes.simulation.devices.temperature_target import TemperatureTarget
from classes.simulation.devices.livingroom_temperature import LivingRoomTemperature
from classes.simulation.devices.heating_cooling import HeatingCooling
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
            time.sleep(0.25)

    def handle_interact(self, address, new_value):
        obj = Object.query \
        .filter_by(address=address) \
        .first()

        for device in self.devices:
            if device.ADDRESS == obj.address:
                if device.INTERACTABLE:
                    current_obj = {"address": device.ADDRESS,
                                   "id": obj.id,
                                   "value": new_value}
                    self.queue.put(json.dumps(current_obj))
                    device.interaction({'value': new_value})
                else:
                    print('Unable to interact with device')
            else:
                print('Unable to interact with device #2')

    def register_device(self, device):
        if isinstance(device, AbstractDevice):
            if device not in self.devices:
                self.devices.append(device)
                if device.DO_MAIN_LOOP:
                    print("DOING IT")
                    self.schedule.every(device.MAIN_LOOP_SCHEDULE).seconds.do(device.main_loop)
        else:
            raise TypeError('Object is not a derivative of AbstractDevice')

    def register_devices_from_database(self):
        objects = Object.query \
        .filter(Object.script_id.isnot(None)) \
        .all()

        self.devices = []
        self.schedule.clear()

        for object in objects:
            if object.script_id == 1:  # Lamp
                device = Lamp(object.name, object.address)
                self.register_device(device)
            if object.script_id == 2:  # Temperature_target
                device = TemperatureTarget(object.name, object.address)
                self.register_device(device)
            if object.script_id == 3:  # Livingroom temperature
                device = LivingRoomTemperature(object.name, object.address)
                self.register_device(device)
            if object.script_id == 4:  # heating_cooling
                device = HeatingCooling(object.name, object.address)
                self.register_device(device)


