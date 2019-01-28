from classes.simulation.abstract.device import AbstractDevice


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
            print(args['value'])

