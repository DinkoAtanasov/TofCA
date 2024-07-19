#!/usr/bin/env python3

import os

import numpy as np

from etc.utils import CfgParser as Parser
from io import StringIO
import pandas as pd


class MpantMpa:
    """
    Class handling the MPANT (mpa) data files!
    Data format is 'asc'
    Updated for newer version: "MCS8A A"
    """
    data = {}
    conf = {'MCS8A': 'MCS8A A', 'MPA4A': 'MPA4A'}

    def __init__(self):
        self.header = {}
        self.version = ''
        self.raw = pd.DataFrame()

    def read(self, mpa):
        """
        Read mpa data file
        :return:
        """
        with open(mpa, 'r') as f:
            fs = f.read()
            self.version = fs[1:6]
            print(self.version)
            name = os.path.basename(mpa).split('.')[0]
            if self.version == 'MPA4A':
                return self.read_asc2d(name, fs)
            elif self.version == 'MCS8A':
                return self.read_asc2d(name, fs)
                # return self.read_ascii(name, fs)

    def parse_header(self, key, txt):
        parser = Parser(strict=False)
        parser.read_file(StringIO(txt))
        tmp = parser.as_dict()
        self.header = dict(**tmp['CHN1'])
        self.header.update(**tmp[key])

    def read_asc2d(self, name, fs):
        raw_header, raw_data = fs.split('[DATA]\n')
        if bool(raw_data) and len(raw_data.split(' ')) >= 9:
            self.parse_header(self.conf[self.version], raw_header)
            caloff = float(self.header['caloff'])
            calfact = float(self.header['calfact'])
            raw = pd.read_csv(StringIO(raw_data), delimiter=' ',
                              usecols=(0, 1, 2), header=0, names=['tof', 'cycles', 'counts'])
            tmp_tofs, tmp_cnts = [], []
            raw['tof [ns]'] = caloff + (raw['tof'] - 0.5) * calfact
            for bin, grp in raw.groupby('tof'):
                tmp_tofs.append(caloff + (int(bin) - 0.5) * calfact)
                tmp_cnts.append(grp['counts'].sum())
            xproj = pd.DataFrame({'tof [ns]': tmp_tofs,'cycles': tmp_tofs, 'counts': tmp_cnts})

            return xproj, raw
            # return raw

    def read_ascii(self, name, fs):
        raw_header, raw_data = fs.split('[TDAT0,')
        self.parse_header(self.conf[self.version], raw_header)
        caloff = float(self.header['caloff'])
        calfact = float(self.header['calfact'])
        bin_range = int(self.header['range'])
        tof_bins = np.arange(0, bin_range-1, 1)
        tof_ns = caloff + (tof_bins - 0.5) * calfact
        raw_data = raw_data.strip(f'{bin_range} ]')
        data = pd.read_csv(StringIO(raw_data), header=0, names=['counts'])
        data['tof [ns]'] = tof_ns
        return data

    def process(self, f):
        return self.read(f)


