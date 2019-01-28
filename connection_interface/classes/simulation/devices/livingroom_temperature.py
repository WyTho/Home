from classes.simulation.abstract.device import AbstractDevice
from models import Object
from config import db


class LivingRoomTemperature(AbstractDevice):
    def __init__(self, name, address):
        super().__init__(name, address)
        self.SCRIPT_ID = 3  # Manual script id for now


    def initialize_device_properties(cls):
        cls.PROTOCOL = 'PROTOCOL'
        cls.DATA_TYPE = 5  # See documentation on data types
        cls.INTERACTABLE = False

        # Other device properties
        cls.MODEL = ''
        cls.INITIAL_VALUE = True
        cls.CONNECTED_DEVICES = ["1/2/0",
                                 "1/2/1"]

    def initialize_device_schedule(cls):
        cls.DO_MAIN_LOOP = True
        cls.MAIN_LOOP_SCHEDULE = 3

    def main_loop(cls):
        heating_cooling = Object.query \
              .filter_by(address=cls.CONNECTED_DEVICES[0]) \
              .first()

        temperature_target = Object.query \
                            .filter_by(address=cls.CONNECTED_DEVICES[1]) \
                            .first()

        myDbObject = Object.query \
                       .filter_by(address=cls.ADDRESS) \
                       .first()

        new_temperature = 0
        target = float(temperature_target.current_value)
        mine = float(myDbObject.current_value)
        new_temperature = mine
        if heating_cooling.current_value == 'True' and mine <= target:  # Heating
            new_temperature = mine + 1

        if heating_cooling.current_value == 'True' and mine >= target:
            new_temperature = mine - 0.1

        if heating_cooling.current_value == 'False' and mine >= target:
            new_temperature = mine - 1

        if heating_cooling.current_value == 'False' and mine <= target:
            new_temperature = mine + 1

        myDbObject.current_value = new_temperature
        db.session.add(myDbObject)
        db.session.commit()


    def interaction(cls, args):
        if 'value' in args:
            print(args['value'])

