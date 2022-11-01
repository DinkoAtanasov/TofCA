#!/usr/bin/env python3

import os
from etc.utils import CfgParser as Parser
import numpy as np
import pandas as pd
from io import StringIO


class Mcdwin():
    """
    Class handling the MCDWIN (.887) data files!
    Data format is 'csv, asc'
    """
    data = {}

    def __init__(self):
        self.header = {}
        self.raw = pd.DataFrame()

    def read(self, p887):
        """
        Read mpa data file
        :return:
        """
        self.parse_header(p887)
        directory = os.path.dirname(p887) + os.path.sep
        print(directory)
        name = os.path.basename(p887).split('.')[0]
        raw = pd.DataFrame()

        if self.header['sweepmode'] == '80' and self.header['fmt'] == 'csv':
            raw = self.read_csv_80(directory, name)
        elif self.header['sweepmode'] == '84' and self.header['fmt'] == 'csv':
            raw = self.read_csv_84(directory, name)
        elif self.header['sweepmode'] == '84' and self.header['fmt'] == 'asc':
            raw = self.read_asc_84(directory, name)
        else:
            del self.header
            return

        # if raw['counts'].sum() != 0:
        raw = raw.drop(raw[raw['counts'] > 0].index)
        return self.tof_proj(raw)

    def tof_proj(self, raw):
        caloff = float(self.header['caloff'])
        calfact = float(self.header['calfact'])
        tmp_tofs, tmp_cnts = [], []
        for bin, grp in raw.groupby('bins'):
            tmp_tofs.append(caloff + (int(bin) - 0.5) * calfact)
            tmp_cnts.append(grp['counts'].sum())
        return pd.DataFrame({'tof [ns]': tmp_tofs, 'counts': tmp_cnts})

    def read_csv_80(self, folder, name):
        self.header['cycles'] = '1'
        fname = folder + name + f'.{self.header["fmt"]}'
        # df = pd.read_csv(fname, sep='\t', header=None, dtype=float, prefix='Y')
        df = pd.read_csv(fname, sep='\t', header=None, usecols=[1], dtype=float, names=['counts'])
        chan = [y for y in range(int(self.header['range']))]
        df['bins'] = chan
        # cycles = [np.full((int(self.header['range'])), i) for i in range(1)]
        # slices = np.concatenate(cycles, axis=0)
        return pd.DataFrame({'bins': np.array(chan), 'counts': df['Y1'].to_numpy()})

    def read_csv_84(self, folder, name):
        fname = folder + name + f'.{self.header["fmt"]}'
        df = pd.read_csv(fname, sep='\t', header=None, usecols=[1], dtype=float, names=['counts'])
        chan = [y for x in range(int(self.header['cycles'])) for y in range(int(self.header['range']))]
        print(len(df['counts']))
        print(len(chan))
        df['bins'] = chan

        return df
        # cycles = [np.full((int(self.header['range'])), i) for i in range(int(self.header['cycles']))]
        # slices = np.concatenate(cycles, axis=0)

        # return pd.DataFrame({'tof': np.array(chan), 'counts': df['Y1'].to_numpy()})

    def read_asc_84(self, folder, name):
        fname = folder + name + f'.{self.header["fmt"]}'
        with open(fname, 'r') as f:
            fs = f.read()
            _, raw_data = fs.split('[DATA]\n')
            if len(raw_data.split(' ')) >= 3:  # If there is data (more than three lines), load it to df
                df = pd.read_csv(StringIO(raw_data), delimiter=' ', usecols=[0, 2], header=None, names=['tof', 'counts'])
            else:  # Else build an empty dummy df
                df = pd.DataFrame({'bins': np.zeros(5),
                                   'counts': np.zeros(5)})
        return df

    def parse_header(self, key):
        with open(key, 'r') as f:
            fs = '[root]\n' + f.read()
            # key = os.path.basename(key).split('.')[0]

            parser = Parser(strict=False)
            parser.read_file(StringIO(fs))
            tmp = parser.as_dict()

            self.header = dict(**tmp['root'])
            # correct for inconsistent 'fmt' keyword in FASTCom configuration file (.887)
            if self.header['fmt'] == '3':
                self.header['fmt_idx'] = '3'
                self.header['fmt'] = 'asc'

    def process(self, mcdwin):
        print(mcdwin)
        return self.read(mcdwin)
