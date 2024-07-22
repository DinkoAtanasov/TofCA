
from etc.mpant import MpantMpa
from etc.mcdwin import Mcdwin
from etc.jyfl import Jyfl
from etc.read_csv import ReadCsv

class DataReader:
    """
    General Class to package all available data readers!
    """
    readers = {
        'mpant': MpantMpa(),
        # 'mcdwin': Mcdwin(),
        'jyfl': Jyfl(),
        'csv': ReadCsv()
    }

    def __init__(self):
        # self.readers = {'mpant': MpantMpa(), 'mcdwin': Mcdwin(), 'jyfl': Jyfl(), 'csv': ReadCsv()}
        self.readers = {'mpant': MpantMpa(), 'jyfl': Jyfl(), 'csv': ReadCsv()}

    def get_data_reader(self, ident):
        """
        Choose a valid data reader class
        :param ident:
        :return:
        """
        print('Reader:: ', ident)
        if ident in self.readers:
            return self.readers[ident]