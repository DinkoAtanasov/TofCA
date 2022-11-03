#!/usr/bin/env python

import os
import sys

from typing import List
from etc.data_reader import DataReader
from etc.constants import FILE_EXTENSION

import pandas as pd

from PyQt5 import QtWidgets, QtCore
from forms.converted import ui_plot_dlg as ui

import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class PlotBrowser(QtWidgets.QDialog, ui.Ui_PlotDialog):
    """
    Class to handle plotting of spectra. Displays where new isobars would appear.
    """

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.raw_exist = False
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        self.data_factory = DataReader()
        self.reader_id = 'csv'

        self.color_identity = {0: 'k', 1: 'r', 2: 'c', 3: 'm', 
                               4: 'g', 5: 'b', 6: 'y', 7: 'c', 
                               8: pg.mkColor(8), 9: pg.mkColor(9),
                               10: pg.mkColor(10), 11: pg.mkColor(11), 12: pg.mkColor(12)}
        self.font = None
        self.stats = None
        self.spectrum = None
        self.pg_raw_item = None
        self.raw_tof = pd.DataFrame()
        self.mca_start = -10_000
        self.mca_stop = 10_000
        self.tof_center = 0
        # self.new_mca_stop()

        self.tofs_table = pd.DataFrame()
        self.tof_widget = pg.PlotWidget()

        self.okButton.clicked.connect(self.my_accept)
        self.cancelButton.clicked.connect(self.reject)
        self.loadButton.clicked.connect(self.load)
        self.tofShiftBox.valueChanged.connect(self.shift_tof)
        self.tofBins.valueChanged.connect(self.new_mca_start)
        self.tofBinWidth.valueChanged.connect(self.new_mca_start)

        self.ini_display()
    
    def ini_display(self):
        px = 22
        self.spectrum = self.tof_widget.getPlotItem()
        self.spectrum.setLabels(title='Identification plot', left='Counts', bottom='time (ns)')
        self.font = self.spectrum.getAxis('bottom').label.font()
        self.font.setPointSize(px)
        self.spectrum.getAxis('bottom').label.setFont(self.font)
        self.spectrum.getAxis('left').label.setFont(self.font)
        self.font.setPointSize(px-4)
        self.spectrum.getAxis('bottom').setStyle(tickFont=self.font)
        self.spectrum.getAxis('left').setStyle(tickFont=self.font)
        self.spectrum.addLegend()
        self.graphWidget.layout().addWidget(self.tof_widget)

    def new_plot_title(self, amass, sym, revs):
        self.spectrum.setTitle(title=f'Identification plot {amass}{sym} @{revs}revs', size='24pt')
        self.spectrum.setLabels(left='Counts', bottom=f'tof - {self.tof_center*1e3:.1f} (ns)')

    def new_table_indent(self, df):
        self.tofs_table = df
        self.tofs_table['tof_copy'] = self.tofs_table['ToF']
        self.tofs_table['Deltas_copy'] = self.tofs_table['Deltas']

    def new_mca_stop(self):
        # self.mca_stop = self.mca_start + self.tofBins.value() * self.tofBinWidth.value()
        self.mca_stop = 0.5 * self.tofBins.value() * self.tofBinWidth.value()
        self.set_limits()

    def new_mca_start(self, val):
        # self.mca_start = val - self.tof_center
        self.mca_start = -0.5 * self.tofBins.value() * self.tofBinWidth.value()
        self.new_mca_stop()

    def show_tofs(self):
        if len(self.tofs_table) == 0:
            return
        for i in range(len(self.tofs_table)):
            # pos = self.tofs_table.at[i, 'ToF'] * 1e3  # convert from micro second to nano second
            pos = self.tofs_table.at[i, 'Deltas'] * 1e3  # convert from micro second to nano second
            sym = self.tofs_table.at[i, 'EL']
            icolor = self.tofs_table.at[i, 'Comment']
            self.add_line(pos, sym, icolor)
        if self.raw_exist:
            self.raw_tof['Deltas'] = self.raw_tof['tof [ns]'] - self.tof_center * 1e3
            self.add_raw_tof()
        self.set_limits()

    def set_limits(self) -> None:
        """Update plot range"""
        self.spectrum.setXRange(self.mca_start, self.mca_stop)

    def my_accept(self) -> None:
        self.accept()

    def clear_previous(self) -> None:
        self.spectrum.clear()

    def add_line(self, xpos: float, sym: str, icolor: int) -> None:
        """
        Add infinite line with attached label at the location of a given tof.

        :param icolor:
        :param xpos: ToF position of the line
        :param sym: element symbol
        """
        color = self.color_identity[icolor]
        v_line = pg.InfiniteLine(pos=xpos, angle=90, pen=pg.mkPen(color, width=3), name=sym)
        txt_vline = pg.InfLineLabel(v_line, text=sym, movable=True, rotateAxis=(1, 0), color=color)
        self.font.setPointSize(20)
        txt_vline.setFont(self.font)
        self.spectrum.addItem(v_line, ignoreBounds=True)

    def shift_tof(self):
        a = self.tofShiftBox.value()
        # self.tofs_table['ToF'] = self.tofs_table['tof_copy'] + (a * 0.001)
        self.tofs_table['Deltas'] = self.tofs_table['Deltas_copy'] + (a * 0.001)
        self.clear_previous()
        self.show_tofs()

    def load(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
        name, file_selector = dlg.getOpenFileName(None, 'Open Raw ToF File', os.getcwd(), FILE_EXTENSION)
        file_selector = file_selector.split('(')[0].strip().lower()
        # Get the appropriate data reader
        reader = self.data_factory.get_data_reader(file_selector)
        # Read the Raw Data and extract subset of parameters
        self.raw_tof = reader.process(name)
        self.raw_tof['Deltas'] = self.raw_tof['tof [ns]'] - self.tof_center * 1e3
        self.run = name.split('/')[-1]
        self.raw_exist = True
        self.add_raw_tof()

    def add_raw_tof(self) -> None:
        """
        Adds the TOF spectrum to the plot.
        :return:
        """
        tofs = self.raw_tof['Deltas'].values.tolist() + [self.mca_stop+self.tofBinWidth.value()]
        self.pg_raw_item = self.spectrum.plot(x=tofs,
                                              y=self.raw_tof['counts'],
                                              pen=pg.mkPen('b', width=2),
                                              stepMode='center',
                                              name=self.run)
        self.set_limits()


def main() -> None:
    """If running in stand-alone mode."""
    app = QtWidgets.QApplication(sys.argv)
    mapp = PlotBrowser()
    mapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
