import numpy as np
import pandas as pd


class ReadCsv:
    """
    Class handling CSV data files, exported from other programs.
    Data format is 'csv'
    """

    def __init__(self):
        self.header = {}
        self.raw = pd.DataFrame()

    def read(self, name):
        """
        Read csv data file holding only two columns (TOF vs COUNTS)
        No header is assumed (skipping the first line).
        :return:
        """
        raw = pd.read_csv(name, skiprows=1, header=0, names=['tof [ns]', 'counts'])
        tof_ns = raw['tof [ns]'].to_numpy()
        nrb_bins = tof_ns.shape[0]
        tof_step = (tof_ns[-1] - tof_ns[0]) / nrb_bins
        tof_ns = np.concatenate([tof_ns, [tof_ns[-1] + tof_step]])
        tof_ns = tof_ns - 0.5*tof_step

        self.header.update({'caloff': tof_ns[0]})
        self.header.update({'calfact': tof_step})
        self.header.update({'range': nrb_bins})
        self.header.update({'cycles': 1})

        return tof_ns, raw['counts'].to_numpy(), None

    def process(self, f):
        return self.read(f)
