import abc


class TCPObserver(abc.ABC):
    __metaclass__ = abc.ABCMeta

    @property
    def notify(self, data):
        print(str(data))
