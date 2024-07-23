#!/usr/bin/env python

import os
import sys

from typing import List
from etc.data_reader import DataReader
from etc.constants import FILE_EXTENSION

import numpy as np
import pandas as pd

from PyQt5 import QtWidgets, QtCore, QtGui
from etc.custom_context_menu import VboxCustomContextMenu as VbCMenu
import etc.utils as utils
from forms.converted import ui_plot_dlg as ui


import pyqtgraph as pg

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class PlotBrowser(QtWidgets.QDialog, ui.Ui_PlotDialog):
    """
    Class to handle plotting of spectra. Displays where new isobars would appear.
    """
    newUserMsg = QtCore.pyqtSignal(object, name='newUserMsg')

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        self.data_factory = DataReader()
        self.reader_id = 'mpant'

        self.color_identity = {0: 'k', 1: 'r', 2: 'c', 3: 'm',
                               4: 'g', 5: 'b', 6: 'y', 7: 'c',
                               8: pg.mkColor(8), 9: pg.mkColor(9),
                               10: pg.mkColor(10), 11: pg.mkColor(11),
                               12: pg.mkColor(12), 13: pg.mkColor(13)}
        self.font = None
        self.stats = None
        self.spectrum = None
        self.run = 'Data'
        self.tof_cnts = None
        self.tof_edges = None
        self.tof2d = None
        self.mca_start = -10_000
        self.mca_stop = 10_000
        self.tof_center = 0
        self.raw_exist = False
        self.is_projected = not self.showImg.isChecked()
        self.is_sliced = False
        self.is_rng_frozen = False
        # self.new_mca_stop()

        self.tofs_table = pd.DataFrame()
        self.tof_widget = pg.PlotWidget(viewBox=VbCMenu(defaultPadding=0.1))

        colors = ['w', 'k', 'g', 'r', 'y', 'b']
        self.xy_cmap = pg.ColorMap(None, colors)
        self.bar = pg.ColorBarItem(colorMap=self.xy_cmap)

        self.okButton.clicked.connect(self.my_accept)
        self.cancelButton.clicked.connect(self.reject)
        self.loadButton.clicked.connect(self.load)
        self.tofShiftBox.valueChanged.connect(self.shift_tof)
        self.tof_widget.getPlotItem().vb.sigCrossHair.connect(self.is_crhr_requested)
        self.tof_widget.getPlotItem().vb.sigGaussFit.connect(self.gauss_fit_requested)
        self.tof_widget.getPlotItem().vb.sigNoneFit.connect(self.remove_fit)
        self.tof_widget.getPlotItem().vb.sigRngFreeze.connect(self.rng_freeze_requested)
        self.tof_widget.getPlotItem().vb.sigSettings.connect(self.file_settings_requested)
        self.tofBins.valueChanged.connect(self.new_mca_start)
        self.tofBinWidth.valueChanged.connect(self.new_mca_start)
        self.sliceCheckBox.stateChanged.connect(self.sliced_image_requested)
        self.showImg.toggled.connect(self.tof_image_requested)

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
        self.sliceBox.valueChanged.connect(self.update_sliced_projection)

    def reset_data_containers(self) -> None:
        self.tof_cnts = None
        self.tof_edges = None
        self.tof2d = None
        self.is_projected = True
        self.is_sliced = False

    def file_settings_requested(self, val: int) -> None:
        keep = ['realtime', 'totalsum', 'sweeps', 'swpreset', 'cycles', 'sweepmode', 'fstchan', 'cmline0']
        settings = [f'{key} = {val}' for key, val in self.reader.header.items() if key in keep]
        pretty_settings = '\n'.join(settings)
        self.newUserMsg.emit(str(pretty_settings))

    def tof_image_requested(self, val: int) -> None:
        self.is_projected = not self.showImg.isChecked()
        if not self.is_projected:
            self.sliceCheckBox.stateChanged.disconnect(self.sliced_image_requested)
        else:
            self.sliceCheckBox.stateChanged.connect(self.sliced_image_requested)
        self.add_raw_tof()

    def sliced_image_requested(self, val: int) -> None:
        self.is_sliced = bool(val)
        self.sliceBox.setEnabled(bool(val))
        self.add_raw_tof()

    def update_sliced_projection(self, val: int) -> None:
        self.add_raw_tof()

    def rng_freeze_requested(self, val: int) -> None:
        self.is_rng_frozen = bool(val)

    def is_crhr_requested(self, new_state: bool) -> None:
        """
        Display reticle (crosshair) and Labels indicating the mouse position on a PyQt.PlotItem
        Locate which VisualTab is selected and used it to add/remove the reticle and labels.
        This function is triggered once the USER selects the Boolean indicator CrossHair.

        :param new_state: not used

        """
        pitem = self.tof_widget.getPlotItem()
        if new_state:
            self.add_cross_hair(pitem)
        else:
            self.rem_cross_hair(pitem)

    def add_cross_hair(self, pitem: pg.PlotItem) -> None:
        """
        Create and adds cross-hairs to pyqtgraph PlotItem.

        :param pitem: pyqtgraph.PlotItem contained in the QSubMdiWindow
        """
        vl = pg.InfiniteLine(angle=90, label='x={value:.3f}', labelOpts={'position': 0.9, 'color': 'k'},
                             movable=False, pen=pg.mkPen('r', width=1), name='XXX')
        hl = pg.InfiniteLine(angle=0, label='y={value:.3f}', labelOpts={'position': 0.9, 'color': 'k'},
                             movable=False, pen=pg.mkPen('r', width=1), name='YYY')
        print(vl.name())
        pitem.addItem(vl, ignoreBounds=True)
        pitem.addItem(hl, ignoreBounds=True)
        pitem.scene().sigMouseMoved.connect(self.mouseMoved)

    def rem_cross_hair(self, pitem: pg.PlotItem) -> None:
        """
        Remove cross-hairs from a pyqtgraph PlotItem.

        :param pitem: pyqtgraph.PlotItem contained in the QSubMdiWindow
        """
        cr_names = ['XXX', 'YYY']
        lines = [line for line in pitem.items if isinstance(line, pg.InfiniteLine) and (line.name() in cr_names)]
        for line in lines:
            pitem.removeItem(line)
        pitem.scene().sigMouseMoved.disconnect(self.mouseMoved)

    def mouseMoved(self, pos: QtCore.QPointF) -> None:
        """
        PyQt mouse events moved on top of PyQtGraph GraphicsView-->PlotItem.
        Intercept the parent class events to allow drawing of PyQtGraph elements.

        :param pos: the current position of the mouse point, which is in local coordinates
        """
        cr_names = ['XXX', 'YYY']
        pitem = self.sender().parent().getPlotItem()
        lines = [ln for ln in pitem.items if isinstance(ln, pg.InfiniteLine) and (ln.name() in cr_names)]
        if pitem.sceneBoundingRect().contains(pos):
            mousePoint = pitem.vb.mapSceneToView(pos)
            lines[0].setPos(mousePoint.x())
            lines[1].setPos(mousePoint.y())

    def gauss_fit_requested(self, is_checked: bool) -> None:
        """
        Slot method for a USER request where a gaussian fit needs to be performed
        for data that is displayed in a pyqtgraph placed inside a QSubMdiWindow.

        :param is_checked: A checkbox indicator viewed in the context menu after right-click on the pyqtgraph ViewBox.
                           ONLY value TRUE will be connected as the trigger is part of an exclusive QActionGroup

        """
        pitem = self.tof_widget.getPlotItem()
        xrange = pitem.viewRange()[0]
        data = [di for di in pitem.listDataItems() if isinstance(di, pg.PlotDataItem)][0].getData()

        opt, cov_mat = utils.fit_simple_gauss(data, xrange)
        unc = np.sqrt(np.diag(cov_mat))
        x = np.linspace(xrange[0], xrange[1], 1000)
        y = utils.gauss(x, *opt)

        pitem.plot(x=x, y=y, pen=pg.mkPen('r', width=2), name='FitLine')

        txt = utils.gauss_parameters(opt, unc)
        self.fit_info.clear()
        self.fit_info.setText(txt)
        # title = pitem.titleLabel.item.toPlainText()
        # pitem.setTitle(title=title + ': ' + txt)

    def remove_fit(self, is_checked: bool) -> None:
        """
        When None is selected in the Fit Menu the USER request present fit to be removed.

        :param is_checked: value will always be True as None is selected in the Context menu
        """
        pitem = self.tof_widget.getPlotItem()

        items_to_remove = [i for i in pitem.listDataItems() if i.name() == 'FitLine']
        # title = pitem.titleLabel.item.toPlainText().split(':')[0]
        # pitem.setTitle(title=title)
        for it in items_to_remove:
            pitem.removeItem(it)
        self.fit_info.clear()

    def new_plot_title(self, amass, sym, revs):
        self.spectrum.setTitle(title=f'Identification plot {amass}{sym} @{revs}revs', size='24pt')
        # self.spectrum.setLabels(left='Counts', bottom=f'tof - {self.tof_center*1e3:.1f} (ns)')
        self.spectrum.setLabels(left='Counts', bottom=f'tof (ns)')

    def new_table_indent(self, df):
        self.tofs_table = df.copy()
        self.tofs_table['tof_copy'] = self.tofs_table['ToF'].copy()
        self.tofs_table['Deltas_copy'] = self.tofs_table['Deltas'].copy()

    def new_mca_stop(self):
        # self.mca_stop = self.mca_start + self.tofBins.value() * self.tofBinWidth.value()
        self.mca_stop = self.acqdelay.value() + self.tofBins.value() * self.tofBinWidth.value()

    def new_mca_start(self):
        self.mca_start = self.acqdelay.value() - 0.5 * self.tofBinWidth.value()
        self.new_mca_stop()

    def show_tofs(self):
        if len(self.tofs_table) == 0:
            return
        for i in range(len(self.tofs_table)):
            pos = self.tofs_table.at[i, 'ToF'] * 1e3  # convert from micro second to nano second
            # pos = self.tofs_table.at[i, 'Deltas'] * 1e3  # convert from micro second to nano second
            mass = self.tofs_table.at[i, 'A']
            sym = self.tofs_table.at[i, 'EL']
            icolor = self.tofs_table.at[i, 'Comment']
            self.add_line(pos, f'{mass}-{sym}', icolor)
        if not self.is_rng_frozen:
            self.set_limits()

    def set_limits(self) -> None:
        """Update plot range"""
        self.new_mca_start()
        self.new_mca_stop()
        self.spectrum.setXRange(self.mca_start, self.mca_stop)

    def my_accept(self) -> None:
        self.accept()

    def clear_previous(self) -> None:
        pitem = self.tof_widget.getPlotItem()
        keep_names = ['XXX', 'YYY', 'FitLine', self.run]
        # cr_names = ['XXX', 'YYY']
        # lines = [line for line in pitem.items if isinstance(line, pg.InfiniteLine) and (line.name() not in cr_names)]
        items = [ln for ln in pitem.items if not isinstance(ln, pg.ImageItem)]
        lines = [line for line in items if line.name() not in keep_names]
        for ln in lines:
            pitem.removeItem(ln)

    def add_line(self, xpos: float, sym: str, icolor: int) -> None:
        """
        Add infinite line with attached label at the location of a given tof.

        :param xpos: ToF position of the line
        :param sym: element symbol
        :param icolor: number to select a color from a dict
        """
        color = self.color_identity[icolor]
        v_line = pg.InfiniteLine(pos=xpos, angle=90, pen=pg.mkPen(color, width=3), name=sym)
        txt_vline = pg.InfLineLabel(v_line, text=sym, movable=True, rotateAxis=(1, 0), color=color)
        self.font.setPointSize(20)
        txt_vline.setFont(self.font)
        self.spectrum.addItem(v_line, ignoreBounds=True)

    def update_tof_location(self) -> None:
        """ Update the locations of the lines following update of the ToF """
        pitem = self.tof_widget.getPlotItem()
        cr_names = ['XXX', 'YYY']
        lines = [line for line in pitem.items if isinstance(line, pg.InfiniteLine) and (line.name() not in cr_names)]
        for line in lines:
            mass, sym = line.name().split('-')
            tof = self.tofs_table[(self.tofs_table['A'] == int(mass)) & (self.tofs_table['EL'] == sym)]['ToF']
            line.setPos(tof.to_numpy()[0] * 1e3)

    def shift_tof(self) -> None:
        """ Adjust the ToF by a User offset """
        a = self.tofShiftBox.value()
        self.tofs_table['ToF'] = self.tofs_table['tof_copy'] + (a * 0.001)
        # self.tofs_table['Deltas'] = self.tofs_table['Deltas_copy'] + (a * 0.001)
        self.update_tof_location()

    def load(self):
        dlg = QtWidgets.QFileDialog(parent=self)
        dlg.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
        name, file_selector = dlg.getOpenFileName(None, 'Open Raw ToF File', os.getcwd(), FILE_EXTENSION)
        if not name:
            return
        self.reset_data_containers()
        file_selector = file_selector.split('(')[0].strip().lower()
        # Get the appropriate data reader
        self.reader = self.data_factory.get_data_reader(file_selector)
        reader = self.reader
        # Read the Raw Data and extract subset of parameters
        self.tof_edges, self.tof_cnts, self.tof2d = reader.process(name)
        self.tofBins.setValue(int(reader.header['range']))
        self.tofBinWidth.setValue(float(reader.header['calfact']))
        self.acqdelay.setValue(float(reader.header['caloff']))
        self.sliceBox.setMaximum(int(reader.header['cycles'])-1)

        self.run = name.split('/')[-1]
        if self.tof2d is not None:
            self.sliceCheckBox.setEnabled(True)
            self.visBox.setEnabled(True)
            self.add_raw_tof()
        else:
            self.sliceCheckBox.setEnabled(False)
            self.sliceCheckBox.setChecked(False)
            self.visBox.setEnabled(False)
            self.showProj.setChecked(True)

    def add_raw_tof(self) -> None:
        """
        Adds the TOF spectrum to the plot.
        :return:
        """

        if self.raw_exist:
            self.remove_raw_spectrum()

        if self.is_projected:
            if self.is_sliced:
                slice = self.sliceBox.value()
                chan = self.tof_edges
                cnts = self.tof2d[:, slice]
            else:
                chan = self.tof_edges
                cnts = self.tof_cnts

            self.spectrum.plot(x=chan, y=cnts, pen=pg.mkPen('b', width=2),
                               stepMode='center', name=self.run)
        else:
            self.add_tof_image()
        self.raw_exist = True
        if not self.is_rng_frozen:
            self.set_limits()

    def add_tof_image(self) -> None:
        """ Display 2D TOF Histogram as PyQtImageItem"""
        if self.tof2d is None:
            self.newUserMsg.emit('No 2D data exists!')
            self.sliceCheckBox.setEnabled(False)
            self.sliceCheckBox.setChecked(False)
            self.visBox.setEnabled(False)
            self.showProj.setChecked(True)
            return
        img = pg.ImageItem()
        img.setImage(self.tof2d)
        tr_xvsy = QtGui.QTransform()
        tof_start = self.acqdelay.value() - 0.5 * self.tofBinWidth.value()
        tr_xvsy.translate(tof_start, 0)
        tr_xvsy.scale(self.tofBinWidth.value(), 1)
        img.setTransform(tr_xvsy)
        self.spectrum.addItem(img)
        self.bar.setImageItem(img, insert_in=self.spectrum)
        self.bar.setLevels(low=0, high=self.tof2d.max())

    def remove_raw_spectrum(self):
        pitem = self.tof_widget.getPlotItem()
        old = [item for item in pitem.items if isinstance(item, pg.PlotDataItem) or isinstance(item, pg.ImageItem)]
        for spec in old:
            pitem.removeItem(spec)
        self.raw_exist = False


def main() -> None:
    """If running in stand-alone mode."""
    app = QtWidgets.QApplication(sys.argv)
    mapp = PlotBrowser()
    mapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
