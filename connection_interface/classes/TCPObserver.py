import abc


class TCPObserver(abc.ABC):
    """Observer for the observer pattern
    
    Arguments:
        abc {[Abstract class]} -- Abstract class implementation
    """
    __metaclass__ = abc.ABCMeta

    @property
    def notify(self, data):
        """Implementable function for observer
        
        Arguments:
            data {[string]} -- String of data
        """
        print(str(data))
