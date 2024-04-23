from abc import *

class DataSource(ABC):
    @abstractmethod
    def get_data(self):
        pass


class DataAgregator(ABC):
    @abstractmethod
    def get_data(self):
        pass
    @abstractmethod
    def process_data(self):
        pass