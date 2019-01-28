from abc import ABC


class AbstractDevice(ABC):
    def __init__(self):
        self.NAME = 'UNKNOWN'
        self.ADDRESS = 'UNKNOWN'
        self.SCRIPT_ID = None   # Manual script id for now
        super().__init__()
        self.initialize_device_properties()
        self.initialize_device_schedule()

    def __init__(self, name, address):
        self.NAME = name
        self.ADDRESS = address
        super().__init__()
        self.initialize_device_properties()
        self.initialize_device_schedule()

    @classmethod
    def initialize_device_properties(cls):
        cls.PROTOCOL = 'PROTOCOL'
        cls.DATA_TYPE = 1  # See documentation on data types
        cls.INTERACTABLE = True

        # Other device properties
        cls.MODEL = ''
        cls.INITIAL_VALUE = True

    @classmethod
    def initialize_device_schedule(cls):
        cls.DO_MAIN_LOOP = True
        cls.MAIN_LOOP_SCHEDULE = 1  # Every second

    @classmethod
    def main_loop(cls):
        return True

    @classmethod
    def interaction(cls, args):
        if(cls.INTERACTABLE):
            print("You can interact with this device")
        else:
            print("You cannot interact with this device")








