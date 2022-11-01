
import pandas as pd


class ReadCsv:
    """
    Class handling the JYFL (txt) data files!
    Data format is 'txt'
    """

    def __init__(self):
        self.header = {}
        self.raw = pd.DataFrame()

    def read(self, name):
        """
        Read mpa data file
        :return:
        """
        return pd.read_csv(name, skiprows=1, header=0, names=['tof [ns]', 'counts'])

    def process(self, f):
        return self.read(f)
