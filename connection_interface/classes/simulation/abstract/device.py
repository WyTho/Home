from abc import ABC


class AbstractDevice(ABC):
    """A basic implementation for a simulation device
    
    Arguments:
        ABC {Abstract Class} -- abc
    """

    def __init__(self):
        """Initializer for AbstractDevice
        """
        self.NAME = 'UNKNOWN'
        self.ADDRESS = 'UNKNOWN'
        self.SCRIPT_ID = None  # Manual script id for now
        super().__init__()
        self.initialize_device_properties()
        self.initialize_device_schedule()

    def __init__(self, name, address):
        """Inializer for AbstractDevice
        
        Arguments:
            name {string} -- Name of the device
            address {string} -- Address of the device(e.g: 0/0/1)
        """
        self.NAME = name
        self.ADDRESS = address
        super().__init__()
        self.initialize_device_properties()
        self.initialize_device_schedule()

    @classmethod
    def initialize_device_properties(cls):
        """Initializes device properties. Please add any other device properties to this function
        """
        cls.PROTOCOL = 'PROTOCOL'
        cls.DATA_TYPE = 1  # See documentation on data types
        cls.INTERACTABLE = True

        # Other device properties
        cls.MODEL = ''
        cls.INITIAL_VALUE = True

    @classmethod
    def initialize_device_schedule(cls):
        """Initializes devices main_loop if needed.
        """
        cls.DO_MAIN_LOOP = True
        cls.MAIN_LOOP_SCHEDULE = 1  # Every second

    @classmethod
    def main_loop(cls):
        """Main loop for the device. Executed as stated in @function initialize_device_schedule
        """
        return True

    @classmethod
    def interaction(cls, args):
        """The interaction method for the device
        
        Arguments:
            args {dictionary} -- Any arguments you may want to send to this device
        """
        if (cls.INTERACTABLE):
            print("You can interact with this device")
        else:
            print("You cannot interact with this device")
