
#!/usr/bin/env python
import os
import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets
from forms.converted import ui_calib_dialog as ui

from etc.mass import Ame
from etc.utils import CfgParser


class IsepCalibration(QtWidgets.QDialog, QtCore.QObject, ui.Ui_CalibIsep):

    mass1: float
    mass2: float
    revs_0: int = 0
    revs_n: int
    tof1: float
    tof2: float
    tof3: float
    tof4: float
    a1: float
    a2: float
    b1: float
    b2: float
    is_existing: bool = False

    # request_mass = QtCore.pyqtSignal(object, name='Ame_request')

    def __init__(self, *args, **kwargs) -> None:
        super(IsepCalibration, self).__init__(*args, **kwargs)

        # Load the UI Page
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        # Load AME Table
        # This class is also loaded in the Main window.
        # One can optimize the calls to AME table in only one location
        self.ame = Ame()

        self.config = None
        self.parser = CfgParser()

        self.signals_button_connect()

    def signals_button_connect(self) -> None:
        self.Tof1Edit.editingFinished.connect(self.get_tof1)
        self.Tof2Edit.editingFinished.connect(self.get_tof2)
        self.Tof3Edit.editingFinished.connect(self.get_tof3)
        self.Tof4Edit.editingFinished.connect(self.get_tof4)
        self.RevsEdit.editingFinished.connect(self.get_revs)
        self.mass1Edit.editingFinished.connect(self.get_mass1)
        self.mass2Edit.editingFinished.connect(self.get_mass2)
        self.calcButton.clicked.connect(self.calc_parameters)
        self.loadButton.clicked.connect(self.load)
        self.saveButton.clicked.connect(self.save)

    def get_tof1(self) -> None:
        self.tof1 = float(self.Tof1Edit.text())

    def get_tof2(self) -> None:
        self.tof2 = float(self.Tof2Edit.text())

    def get_tof3(self):
        self.tof3 = float(self.Tof3Edit.text())

    def get_tof4(self) -> None:
        self.tof4 = float(self.Tof4Edit.text())

    def get_revs(self) -> None:
        self.revs_n = int(self.RevsEdit.text())

    def get_mass1(self) -> None:
        mass_str = self.mass1Edit.text()
        charge = int(self.charge1Edit.text().strip())
        self.mass1, *_ = self.ame.get_ion_mass(mass_str, charge)
        # Returned mass is in micro-u
        self.mass1 = float(self.mass1) * 1e-6

    def get_mass2(self) -> None:
        mass_str = self.mass2Edit.text()
        charge = int(self.charge2Edit.text().strip())
        self.mass2, *_ = self.ame.get_ion_mass(mass_str, charge)
        # Returned mass is in micro-u
        self.mass2 = float(self.mass2) * 1e-6

    def verify_input_fields(self) -> bool:
        """Verify that all fields required in the calculation are valid inputs."""
        ok = True if self.mass1Edit.text().isalnum() else False
        ok = True if ok and self.mass2Edit.text().isalnum() else False
        ok = True if ok and self.Tof1Edit.text() != '' else False
        ok = True if ok and self.Tof2Edit.text() != '' else False
        ok = True if ok and self.Tof3Edit.text() != '' else False
        ok = True if ok and self.Tof4Edit.text() != '' else False
        return ok

    def calc_parameters(self) -> None:
        """Calculate ISEP calibration parameters"""
        if not self.verify_input_fields():
            print('An input field is empty! Please fill in the Masses and ToFs for both 1 and N revs.')
            return
        self.a1 = (self.tof1 - self.tof2) / (np.sqrt(self.mass1) - np.sqrt(self.mass2))
        self.b1 = self.tof1 - self.a1 * np.sqrt(self.mass1)
        # b1 = self.tof2 - self.a1 * np.sqrt(self.mass2)

        self.a2 = (self.tof3 - self.tof4) / (np.sqrt(self.mass1) - np.sqrt(self.mass2))
        self.b2 = self.tof3 - self.a2*np.sqrt(self.mass1)

        self.a1CalibEdit.setText(f'{self.a1:.5f}')
        self.b1CalibEdit.setText(f'{self.b1:.5f}')

        self.a2CalibEdit.setText(f'{self.a2:.5f}')
        self.b2CalibEdit.setText(f'{self.b2:.5f}')

        self.is_existing = True

    def load(self) -> None:
        """
        Reads the MRTOF calibration parameters.
        """
        dlg = QtWidgets.QFileDialog()
        name = dlg.getOpenFileName(None, 'Open Calibration', os.getcwd(), 'Config file (*.ini)')[0]

        self.parser.read(name)
        config = self.parser.as_dict()

        self.mass1Edit.setText(config['RefMasses']['mass1'])
        self.mass1Edit.editingFinished.emit()
        self.charge1Edit.setText(config['RefMasses']['charge1'])
        self.mass2Edit.setText(config['RefMasses']['mass2'])
        self.mass2Edit.editingFinished.emit()
        self.charge2Edit.setText(config['RefMasses']['charge2'])

        self.Tof1Edit.setText(config['RefTofs']['tof1'])
        self.Tof1Edit.editingFinished.emit()
        self.Tof2Edit.setText(config['RefTofs']['tof2'])
        self.Tof2Edit.editingFinished.emit()
        self.Tof3Edit.setText(config['RefTofs']['tof3'])
        self.Tof3Edit.editingFinished.emit()
        self.Tof4Edit.setText(config['RefTofs']['tof4'])
        self.Tof4Edit.editingFinished.emit()

        self.RevsEdit.setText(config['RefTofs']['revsn'])
        self.RevsEdit.editingFinished.emit()

        self.calcButton.click()

    def save(self) -> None:
        """Save the current calibration parameters"""
        config = {'RefMasses': {'mass1': self.mass1Edit.text(),
                                'charge1': self.charge1Edit.text(),
                                'mass2': self.mass2Edit.text(),
                                'charge2': self.charge2Edit.text()},
                  'RefTofs': {'tof1': self.Tof1Edit.text(),
                              'tof2': self.Tof2Edit.text(),
                              'tof3': self.Tof3Edit.text(),
                              'tof4': self.Tof4Edit.text(),
                              'revsn': self.RevsEdit.text()}
                  }

        dlg = QtWidgets.QFileDialog()
        name = dlg.getSaveFileName(None, 'Save Calibration', os.getcwd(), 'Config file (*.ini)')[0]

        self.parser.dict_to_parser(config)
        with open(name, 'w') as configfile:
            self.parser.write(configfile)


def main() -> None:
    """If running in stand-alone mode."""
    app = QtWidgets.QApplication(sys.argv)
    mapp = IsepCalibration()
    mapp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
