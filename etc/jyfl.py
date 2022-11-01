
import pandas as pd


class Jyfl:
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
        return pd.read_csv(name, skiprows=27, sep='\t', header=0, names=['tof [ns]', 'counts'])

    def process(self, f):
        return self.read(f)
