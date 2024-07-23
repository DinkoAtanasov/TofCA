#!/usr/bin/env python3

import os

import numpy as np

from etc.utils import CfgParser as Parser
from etc.utils import fill_hist_nb, hist2d_numba_seq
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
            name = os.path.basename(mpa).split('.')[0]
            raw = self.read_asc2d(name, fs)
            return *self.tof_proj(raw), self.tof_2d(raw)

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
            raw = pd.read_csv(StringIO(raw_data), delimiter=' ',
                              usecols=(0, 1, 2), header=0, names=['tof', 'cycles', 'counts'])
            return raw

    def read_tdat0(self, name, fs):
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

    def process(self, f):
        return self.read(f)


