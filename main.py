# -*- coding: utf-8 -*-

# import os
import sys
import numpy as np
import pandas as pd

from PyQt5 import QtCore, QtWidgets, QtGui
from forms.converted import ui_main as ui

from etc.constants import *
from etc.mass import Ame
from etc.calib_isep import IsepCalibration
from etc.extras import AddExtra
from etc.plotting import PlotBrowser

from typing import Any, List

# Column names and where to be placed in the table view.
col_names = {'A': 0, 'EL': 1, 'ME': 4, 'MEunc': 5, 'm/q': 6, 
             'Center': 7, 'MagneTof': 8, 'RevTime': 9, 'ISEPtrap': 10,
             'ToF': 2, 'DAQ delay': 11, 'Deltas': 3, 'Check': 12}
col_units = {'A': '', 'EL': '', 'ME': '/ keV', 'MEunc': '/ keV', 'm/q': '',
             'Center': '/ us', 'MagneTof': '/ us', 'RevTime': '/ us',
             'ISEPtrap': '/ us', 'ToF': '/ us', 'DAQ delay': ' / ns',
             'Deltas': ' / ns', 'Check': ' / ns'}


class IsepBrowser(QtWidgets.QMainWindow, QtCore.QObject, ui.Ui_MainWindow):
    """
    
    """

    def __init__(self, *args, **kwargs) -> None:
        super(IsepBrowser, self).__init__(*args, **kwargs)

        # Load the UI Page
        self.idx = None
        self.setupUi(self)
        self.isobars = pd.DataFrame()
        self.calibration = IsepCalibration()
        self.ame = Ame()
        self.add_extras = AddExtra()

        self.idn = {'isobars': 0}
        extra_id = list(self.add_extras.ident.keys())[1:]
        for i, option in enumerate(extra_id, start=1):
            self.idn.update({option: i})

        self.plt = PlotBrowser()
        self.new_element_entered = False
        self.a = 85
        self.el = 'Rb'
        self.z = 37

        self.table_headers()

        # connect signals
        self.actionCalibration.triggered.connect(self.calibration.show)
        self.actionAddExtra.triggered.connect(self.add_extras.show)
        self.actionQuit.triggered.connect(self.plt.close)
        self.actionQuit.triggered.connect(self.calibration.close)
        self.add_extras.extras_ready.connect(self.extra_selection)
        self.tableShowButton.clicked.connect(self.new_mass)
        self.reqMassEdit.editingFinished.connect(self.element_modified)
        self.reqNRevsBox.valueChanged.connect(self.on_user_change)
        self.checkTofBox.valueChanged.connect(self.check_tof)
        self.showSpectrum.toggled.connect(self.react_to_toggle)
        self.round_fact_ppg.valueChanged.connect(self.cavity_rounding)
        self.round_fact_mcs.valueChanged.connect(self.mcs_rounding)
        #
        self.plt.tofBins.valueChanged.connect(self.on_user_change)
        self.plt.tofBinWidth.valueChanged.connect(self.on_user_change)
        self.plt.showSettings.connect(self.show_msg)
    
    ############################################################################
    # Methods related to Time of flight calculations
    ############################################################################

    def calculate_tof(self, dframe: pd.DataFrame) -> None:
        """
        Calculate TOF from loaded calibration parameters.
        Note that the AME class holds the total atomic mass in micro-u units.
        :param dframe: DataFrame holding information about the isotopes of interest
        :return: None
        """
        if len(dframe) == 0:
            self.show_msg('No mass existing in AME table. Calculation stopped!')
            return
        dframe['m/q'] = (dframe['ame_tot'] - dframe['charge'] * self.ame.me) / dframe['charge']
        dframe['m/q'] = dframe['m/q'] * 1e-6
        a0 = self.calibration.a1
        b0 = self.calibration.b1
        a1 = self.calibration.a2
        b1 = self.calibration.b2
        ncal = float(self.calibration.revs_n)
        nrevs = float(self.reqNRevsBox.value())
        binwidth = self.plt.tofBinWidth.value()
        bins = self.plt.tofBins.value()
        half_window = (binwidth * bins) / 2  # AcqDelay for minimum half the Tof Range in ns
        # self.plt.mca_start = -half_window

        dframe['ShTr'] = a0 * np.sqrt(dframe['m/q']) + b0
        dframe['Center'] = dframe['ShTr'] * DIST_BUNCHER_TO_CAVITY
        # dframe['MagneTof'] = dframe['ShTr'] * (1-DIST_BUNCHER_TO_CAVITY)
        dframe['MagneTof'] = dframe['ShTr'] * DIST_CAVITY_TO_MCP
        dframe['Offset'] = dframe['ShTr'] * OFFSET
        dframe['AllFactors'] = dframe['Center'] + dframe['MagneTof'] + dframe['Offset']
        # trapping time in the MR-ToF-ms for n number of revs
        dframe['ISEPtrap'] = (nrevs/ncal) * (a1 * np.sqrt(dframe['m/q']) + b1 - dframe['AllFactors'])
        dframe['ToF'] = dframe['ISEPtrap'] + dframe['AllFactors']
        dframe['RevTime'] = dframe['ISEPtrap'] / nrevs
        dframe['DAQ delay'] = dframe['ToF']*1e3 - half_window
        dframe['Check'] = dframe['ToF']*1e3 - self.checkTofBox.value()

    def delta_tof(self) -> None:
        """Add to DataFrame the Delta ToFs of isobars wrt to the requested mass."""
        df = self.isobars
        sym = self.el
        anum = int(self.a)
        if len(df) == 0:
            return
        self.idx = df[(df['EL'] == sym) & (df['A'] == anum)]['ToF'].index.to_list()[0]
        itof = df[(df['EL'] == sym) & (df['A'] == anum)]['ToF'].values[0]
        df['Deltas'] = df['ToF'] - itof
        self.plt.tof_center = itof

    def check_tof(self) -> None:
        """Add values for Delta ToFs wrt the CheckToF value set in the GUI."""
        df = self.isobars
        df['Check'] = df['ToF'] * 1e3 - self.checkTofBox.value()
        for i in range(len(df)):
            self.Table.setItem(i, 12, QtWidgets.QTableWidgetItem(f'{df.at[i, "Check"]:.3f}'))
        self.highlight_tofs(self.idx)

    ############################################################################
    # Methods related to Atomic mass evaluation
    ############################################################################

    def new_mass(self) -> None:
        """Slot for the signal changing the requested mass."""
        self.element_modified()
        if not self.new_element_entered:
            return
        if not self.calibration.is_existing:
            msg = 'Calibration does not exist! Load it from Menu->Calibration.'
            self.show_msg(msg)
            return
        self.el, _, self.a, self.z = self.ame.evaluate_expr(self.reqMassEdit.text(), flag=True)
        self.ame_selection()

    def ame_selection(self) -> None:
        """Select isobars from AME to use in ToF calculations."""
        self.isobars = pd.DataFrame()
        if self.el not in self.ame.df['EL'].to_list():
            self.ame.add_entry_table(self.el)
        self.isobars = self.ame.df[self.ame.df['A'] == int(self.a)].copy().reset_index()
        self.identify_elements('isobars', self.isobars)
        self.on_user_change()

    def extra_selection(self, info: List) -> None:
        """
        Handle the extra AME selection such as 2+, Oxides, Hydride, Fluorides
        from the Add Extra dialog window.
        :return: None
        """
        who, label = info

        if who == 'select':
            return
        elif who == 'n-charged':
            _, q = label.split('=')
            q = int(q)
            extras = self.ame_query('A', q * int(self.a))
            extras = self.non_matching_labels(extras)
            extras['charge'] = q * extras['charge']
        elif who == 'custom':
            extras = self.ame_query('EL', label)
            if len(extras) == 0:
                self.ame.add_entry_table(label)
                extras = self.ame_query('EL', label)
                extras = self.non_matching_labels(extras)
        elif who == 'isomers':
            expr, ex_erg = label.split('+')
            if '?' in ex_erg:
                ex_erg = ex_erg.strip('?')
            print(expr, float(ex_erg))
            extras = self.ame.calc_isomer_mass(expr, float(ex_erg))
        elif who == 'mass-range':
            vmin, vmax = label.split('-')
            extras = self.ame_query_range('A', int(vmin), int(vmax), ('MinMass', True))
            print(extras)
        else:
            expr, a2 = label.split(';')
            aeff = int(self.a) - int(a2)
            extras = self.ame_query('A', aeff)
            extras['EL'] = '1' + extras["EL"] + str(int(self.a)-int(a2)) + expr
            extras['ame_tot'] = extras['EL'].apply(self.ame.get_extra_mass)
            self.ame.update_mass_excess(extras, int(self.a))
        self.identify_elements(who, extras)
        self.calculate_tof(extras)
        self.isobars = pd.concat([self.isobars, extras], sort=True, ignore_index=True)
        self.delta_tof()
        self.populate_browser(self.isobars)
        self.change_plt()

    def identify_elements(self, el_id: str, dframe) -> None:
        dframe['Comment'] = np.full_like(dframe['A'].to_numpy(), self.idn[el_id], dtype=int)

    def non_matching_labels(self, extra_frame: pd.DataFrame) -> pd.DataFrame:
        """Check for existing isobars or molecules in AME"""
        alist = self.isobars['EL'].to_list()
        blist = extra_frame['EL'].to_list()
        match = [el for el in blist if el in alist]
        for matched in match:
            index = extra_frame[extra_frame['EL'] == matched].index
            extra_frame.drop(index, inplace=True)
        return extra_frame

    def ame_query(self, name: str, val: Any) -> pd.DataFrame:
        return self.ame.df[self.ame.df[name] == val].copy().reset_index()

    def ame_query_range(self, name: str, val_min: Any, val_max: Any, ext_cond: tuple) -> pd.DataFrame:
        cond1 = self.ame.df[name] > val_min
        cond2 = self.ame.df[name] < val_max
        cond3 = self.ame.df[ext_cond[0]] == ext_cond[1]
        return self.ame.df[cond1 & cond2 & cond3].copy().reset_index()

    ############################################################################
    # Methods related to GUI interaction/visualisation
    ############################################################################

    def populate_browser(self, dframe: pd.DataFrame) -> None:
        """
        Reset the Table that will contain the isobars, oxides and dioxides etc.
        Displays new query in the Table.

        :param dframe: Frame containing Time of Flights for given masses
        """

        self.table_reset()
        self.Table.setSortingEnabled(False)
        self.Table.setRowCount(len(dframe))
        for i in range(len(dframe)):
            for key, val in col_names.items():
                if key in 'AELMEMEunc':
                    self.Table.setItem(i, val, QtWidgets.QTableWidgetItem(f'{dframe.at[i, key]}'))
                else:
                    self.Table.setItem(i, val, QtWidgets.QTableWidgetItem(f'{dframe.at[i, key]:.3f}'))        

        self.highlight_tofs(self.idx)
        self.Table.setSortingEnabled(True)
        self.set_info_user()
        self.element_modified()

    def table_headers(self):
        self.Table.setColumnCount(len(col_names.keys()))
        for prefix, col in col_names.items():
            name = f'{prefix}\n{col_units[prefix]}'
            self.Table.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(name))

    def table_reset(self) -> None:
        """Clear/Reset the Table displaying contaminants."""
        self.Table.clear()
        self.table_headers()

    def react_to_toggle(self, state: bool) -> None:
        if state:
            self.plt.show()
        else:
            self.plt.hide()

    def element_modified(self) -> None:
        a_el = str(self.a) + self.el
        self.new_element_entered = False if self.reqMassEdit.text() == a_el else True

    def on_user_change(self) -> None:
        if not self.calibration.is_existing:
            self.show_msg('Calibration does not exist! Please load it from Calibration menu.')
            return
        self.calculate_tof(self.isobars)
        self.delta_tof()
        # self.check_tof()
        self.populate_browser(self.isobars)
        self.change_plt()    

    def change_plt(self):
        self.plt.new_table_indent(self.isobars)
        self.plt.new_plot_title(self.a, self.el, self.reqNRevsBox.value())
        self.plt.clear_previous()
        self.plt.show_tofs()
        self.plt.shift_tof()

    def highlight_tofs(self, row) -> None:
        """highlight the row with Requested mass"""
        for _, col in col_names.items():
            self.Table.item(row, col).setBackground(QtGui.QBrush(QtCore.Qt.yellow))

    def set_info_user(self) -> None:
        """Set values in the Check info section of the GUI"""
        df = self.isobars
        index = self.idx
        self.centerCavityBox.setValue(df.at[index, 'Center'])
        self.isepTrappingBox.setValue(df.at[index, 'ISEPtrap'])
        self.totalTofBox.setValue(df.at[index, 'ToF'])
        self.mcsDelayBox.setValue(df.at[index, 'DAQ delay'])
        # self.plt.new_mca_start(df.at[index, 'DAQ delay'])
        self.set_rounding()

    def set_rounding(self) -> None:
        self.cavity_rounding(self.round_fact_ppg.value())
        self.mcs_rounding(self.round_fact_mcs.value())

    def cavity_rounding(self, factor) -> None:
        cav_center = self.rounding(self.centerCavityBox.value() * 1e3, factor) / 1e3
        self.roundedCenterCavityBox.setValue(cav_center)
        cav_trap = self.rounding(self.isepTrappingBox.value() * 1e3, factor) / 1e3
        self.roundedIsepTrappingBox.setValue(cav_trap)

    def mcs_rounding(self, factor) -> None:
        mcs_del = self.rounding(self.mcsDelayBox.value() * 10,  factor * 10) / 10
        self.roundedMcsDelayBox.setValue(mcs_del)
        if not self.plt.raw_exist:
            self.plt.acqdelay.setValue(mcs_del)

    def rounding(self, value: float, factor: float) -> float:
        return np.round(value / factor) * factor

    def keyPressEvent(self, event):
        """Overload the Qt keyPressEvent with action to delete row(s) from the QTableWidget."""
        # if event.key() == QtCore.Qt.Key_Delete:
        if event.key() == QtCore.Qt.Key_Backspace:
            for index in sorted(self.Table.selectionModel().selectedRows(), reverse=True):
                row = index.row()
                isym = self.Table.item(row, col_names['EL']).text()
                ianum = self.Table.item(row, col_names['A']).text()
                self.drop_elements(isym, int(ianum))
                self.Table.removeRow(row)
            self.on_user_change()
        if event.key() == QtCore.Qt.Key_Enter:
            self.new_mass()
        else:
            super().keyPressEvent(event)

    def drop_elements(self, sym: str, anum: int) -> None:
        """Drops a given row from the DataFrame"""
        df = self.isobars.copy()
        # sym = df.at[row, 'EL']
        # anum = df.at[row, 'A']
        idx = df[(df['EL'] == sym) & (df['A'] == anum)]['ToF'].index.to_list()[0]
        self.isobars = df.drop(index=idx).reset_index(drop=True)

    def show_msg(self, message: str) -> None:
        """
        Open QMessage Information window to USER and display message.

        :param message: String containing the message to be displayed
        """
        print(message)
        title = f'Info::{self.sender().objectName()}'
        reply = QtWidgets.QMessageBox.information(self, title, message,
                                                  QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # the clicked button is returned, if needed to adjust the code following the USER decision


def main():
    app = QtWidgets.QApplication(sys.argv)
    mapp = IsepBrowser()
    mapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
