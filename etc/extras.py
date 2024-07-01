#!/usr/bin/env python

from PyQt5 import QtWidgets, QtCore
from forms.converted import ui_add_dialog as ui


class AddExtra(QtWidgets.QDialog, ui.Ui_add_dlg):
    extras_ready = QtCore.pyqtSignal(object, name='newExtras')

    ident = {'select': 'none',
             'n-charged': 'q=2',
             'isomers': 'AXX+500?',
             'hydrides': ':1H1;1',
             'oxides': ':1O16;16', 
             'fluorides': ':1F19;19',
             'hydro-oxides': ':1H1: 1O16;17', 
             'fluorides-oxides': ':1F19: 1O16;35', 
             'chlorides-35': ':1Cl35;35',
             'chlorides-37': ':1Cl37;37',
             'nitrite-14': ':1N14;14', 
             'nitrite-15': ':1N15;15',
             'mass-range': 'XA-YA',
             'custom': ''
             }

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.ok.clicked.connect(self.new_selection)
        self.cancel.clicked.connect(self.reject)
        self.comboBox.addItems(self.ident.keys())
        self.comboBox.setCurrentIndex(0)
        self.customEdit.setText(self.ident['select'].lower())
        self.comboBox.activated[str].connect(self.on_activated)

    def on_activated(self, text):
        self.customEdit.setText(self.ident[text.lower()])

    def new_selection(self):
        self.extras_ready.emit([self.comboBox.currentText().lower(), self.customEdit.text()])
        self.accept()