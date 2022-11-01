#!/usr/bin/env python3

import os
from etc.utils import CfgParser as Parser
from io import StringIO
import pandas as pd


class MpantMpa:
    """
    Class handling the MPANT (mpa) data files!
    Data format is 'asc'
    """
    data = {}

    def __init__(self):
        self.header = {}
        self.raw = pd.DataFrame()

    def read(self, mpa):
        """
        Read mpa data file
        :return:
        """
        with open(mpa, 'r') as f:
            fs = f.read()
            name = os.path.basename(mpa).split('.')[0]
            raw_header, raw_data = fs.split('[DATA]\n')
            if bool(raw_data) and len(raw_data.split(' ')) >= 9:
                self.parse_header(name, raw_header)
                caloff = float(self.header['caloff'])
                calfact = float(self.header['calfact'])
                raw = pd.read_csv(StringIO(raw_data), delimiter=' ',
                                  usecols=(0, 2), header=0, names=['tof', 'counts'])
                tmp_tofs, tmp_cnts = [], []
                for bin, grp in raw.groupby('tof'):
                    tmp_tofs.append(caloff + (int(bin) - 0.5) * calfact)
                    tmp_cnts.append(grp['counts'].sum())
                return pd.DataFrame({'tof [ns]': tmp_tofs, 'counts': tmp_cnts})

    def parse_header(self, key, txt):
        parser = Parser(strict=False)
        parser.read_file(StringIO(txt))
        tmp = parser.as_dict()
        self.header = dict(**tmp['CHN1'])
        self.header.update(**tmp['MPA4A'])

    def process(self, f):
        return self.read(f)


