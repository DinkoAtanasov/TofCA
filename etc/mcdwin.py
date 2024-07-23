#!/usr/bin/env python3

import os
from etc.utils import CfgParser as Parser
from etc.utils import fill_hist_nb, hist2d_numba_seq
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
        Read p887 data file.
        :return:
        """
        self.parse_header(p887)
        directory = os.path.dirname(p887) + os.path.sep
        name = os.path.basename(p887).split('.')[0]
        raw = pd.DataFrame()

        if self.header['sweepmode'] == '80' and self.header['fmt'] == 'csv':
            raw = self.read_csv_80(directory, name)
            return *self.tof_proj(raw), None
        elif self.header['sweepmode'] == '84' and self.header['fmt'] == 'csv':
            raw = self.read_csv_84(directory, name)
            return *self.tof_proj(raw), self.tof_2d(raw)
        elif self.header['sweepmode'] == '84' and self.header['fmt'] == 'asc':
            raw = self.read_asc_84(directory, name)
            return *self.tof_proj(raw), self.tof_2d(raw)

    def tof_proj(self, raw):
        mca_bins = int(self.header['range'])
        caloff = float(self.header['caloff'])
        calfact = float(self.header['calfact'])

        bins_1d = np.asarray((mca_bins,)).astype(np.int64)
        tof_limits = np.asarray((0, mca_bins)).astype(np.float64)
        proj_cnts = np.zeros(bins_1d, dtype=np.float64)
        tof_ns = caloff + (np.arange(0, mca_bins + 1, 1) - 0.5) * calfact
        fill_hist_nb(proj_cnts, raw['tof'], raw['counts'], bins_1d, tof_limits)
        return tof_ns, proj_cnts

    def tof_2d(self, raw):
        mca_bins = int(self.header['range'])
        cycles_bins = int(self.header['cycles'])

        bins_2d = np.asarray((mca_bins, cycles_bins)).astype(np.int64)
        rng = np.asarray(((0, mca_bins), (0, cycles_bins))).astype(np.float64)
        xyimg = np.zeros((bins_2d[0], bins_2d[1]), dtype=np.float64)
        hist2d_numba_seq(xyimg,
                         raw['tof'].to_numpy().astype(np.float64),
                         raw['cycles'].to_numpy().astype(np.float64),
                         raw['counts'].to_numpy().astype(np.int64),
                         bins_2d,
                         rng)
        return xyimg

    def read_csv_80(self, folder, name):
        self.header['cycles'] = '1'
        fname = folder + name + f'.{self.header["fmt"]}'
        # df = pd.read_csv(fname, sep='\t', header=None, dtype=float, prefix='Y')
        df = pd.read_csv(fname, sep='\t', header=None, usecols=[1], dtype=float, names=['counts'])
        chan = [y for y in range(int(self.header['range']))]
        df['tof'] = np.array(chan)
        # cycles = [np.full((int(self.header['range'])), i) for i in range(1)]
        # slices = np.concatenate(cycles, axis=0)
        return df

    def read_csv_84(self, folder, name):
        fname = folder + name + f'.{self.header["fmt"]}'
        df = pd.read_csv(fname, sep='\t', header=None, usecols=[1], dtype=float, names=['counts'])
        mca_bins = int(self.header['range'])
        max_cycles = int(self.header['cycles'])
        tof_ch = [y for x in range(max_cycles) for y in range(mca_bins)]
        cyc_ch = [y for x in range(mca_bins) for y in range(max_cycles)]
        df['tof'] = np.array(tof_ch)
        df['cycles'] = np.array(cyc_ch)

        return df

    def read_asc_84(self, folder, name):
        fname = f'{folder}{name}.{self.header["fmt"]}'
        with open(fname, 'r') as f:
            fs = f.read()
            _, raw_data = fs.split('[DATA]\n')
            df = pd.read_csv(StringIO(raw_data), delimiter=' ', usecols=[0, 1, 2],
                             header=None, names=['tof', 'cycles', 'counts'])
        return df

    def parse_header(self, key):
        with open(key, 'r') as f:
            fs = '[root]\n' + f.read()
            parser = Parser(strict=False)
            parser.read_file(StringIO(fs))
            tmp = parser.as_dict()

            self.header = dict(**tmp['root'])
            # correct for inconsistent 'fmt' keyword in FASTCom configuration file (.887)
            if self.header['fmt'] == '3':
                self.header['fmt_idx'] = '3'
                self.header['fmt'] = 'asc'

    def process(self, mcdwin):
        return self.read(mcdwin)
