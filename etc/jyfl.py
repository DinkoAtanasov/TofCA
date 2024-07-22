from io import StringIO

import json

import numpy as np
import pandas as pd

HEAD_LEN = 27


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
        self.parse_header(name)
        raw = pd.read_csv(name, skiprows=HEAD_LEN, sep='\t', header=0, names=['tof [ns]', 'counts'])
        val_last_edge = self.header['histogram']['high'] + self.header['calfact']
        tof_ns = np.concatenate([raw['tof [ns]'].to_numpy(), [val_last_edge]])
        tof_ns = tof_ns - 0.5 * self.header['calfact']
        proj_cnts = raw['counts'].to_numpy()
        return tof_ns, proj_cnts, None

    def parse_header(self, name):
        with open(name, 'r') as f:
            lines = [next(f).strip('#').strip('\n') for x in range(HEAD_LEN)]
            raw_header = ''.join(lines)
        self.header = json.loads(raw_header)
        self.header.update({'range': int(self.header['histogram']['binCount'])})
        self.header.update({'calfact': float(self.header['histogram']['binWidth'])})
        self.header.update({'caloff': float(self.header['histogram']['low'])})
        self.header.update({'cycles': 1})

    def process(self, f):
        return self.read(f)
