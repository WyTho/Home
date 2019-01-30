from classes.simulation.abstract.device import AbstractDevice
from models import Object
import requests


class Lamp(AbstractDevice):
    def __init__(self, name, address):
        super().__init__(name, address)
        self.SCRIPT_ID = 1  # Manual script id for now


    def initialize_device_properties(cls):
        cls.PROTOCOL = 'PROTOCOL'
        cls.DATA_TYPE = 2  # See documentation on data types
        cls.INTERACTABLE = True

        # Other device properties
        cls.MODEL = ''
        cls.INITIAL_VALUE = True

    def initialize_device_schedule(cls):
        cls.DO_MAIN_LOOP = False
        cls.MAIN_LOOP_SCHEDULE = False

    def interaction(cls, args):
        if 'value' in args:
            obj = Object.query \
                  .filter_by(address=cls.ADDRESS) \
                  .first()
            print(args['value'])
            data = 0
            if args['value'] == 'True' or args['value'] == '1' or args['value'] == True or args['value'] == 1:
                data = 1
            if args['value'] == 'False' or args['value'] == '0' or args['value'] == False or args['value'] == 0:
                data = 0

            payload = {'usage_id': obj.id, 'data_type': 'TOGGLE', 'data': data}
            events_endpoint = 'http://172.20.10.3:5000/api/v1/events'
            events_response = requests.post(events_endpoint, data=payload)
            print(events_endpoint)

