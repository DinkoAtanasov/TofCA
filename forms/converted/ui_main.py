# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1136, 514)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frameInputs = QtWidgets.QFrame(self.centralwidget)
        self.frameInputs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameInputs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameInputs.setObjectName("frameInputs")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameInputs)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.line = QtWidgets.QFrame(self.frameInputs)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 2)
        self.checkTofBox = QtWidgets.QDoubleSpinBox(self.frameInputs)
        self.checkTofBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.checkTofBox.setProperty("showGroupSeparator", False)
        self.checkTofBox.setDecimals(1)
        self.checkTofBox.setMaximum(1000000000.0)
        self.checkTofBox.setProperty("value", 0.0)
        self.checkTofBox.setObjectName("checkTofBox")
        self.gridLayout_2.addWidget(self.checkTofBox, 4, 1, 1, 1)
        self.reqNRevsBox = QtWidgets.QSpinBox(self.frameInputs)
        self.reqNRevsBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.reqNRevsBox.setMaximum(99999999)
        self.reqNRevsBox.setProperty("value", 1000)
        self.reqNRevsBox.setObjectName("reqNRevsBox")
        self.gridLayout_2.addWidget(self.reqNRevsBox, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frameInputs)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 2)
        self.reqMassEdit = QtWidgets.QLineEdit(self.frameInputs)
        self.reqMassEdit.setObjectName("reqMassEdit")
        self.gridLayout_2.addWidget(self.reqMassEdit, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frameInputs)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frameInputs)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frameInputs)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.tableShowButton = QtWidgets.QPushButton(self.frameInputs)
        self.tableShowButton.setObjectName("tableShowButton")
        self.gridLayout_2.addWidget(self.tableShowButton, 5, 0, 1, 2)
        self.showSpectrum = QtWidgets.QRadioButton(self.frameInputs)
        self.showSpectrum.setObjectName("showSpectrum")
        self.gridLayout_2.addWidget(self.showSpectrum, 6, 0, 1, 2)
        self.gridLayout_3.addWidget(self.frameInputs, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 3, 1, 1)
        self.frameOutputs = QtWidgets.QFrame(self.centralwidget)
        self.frameOutputs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOutputs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOutputs.setObjectName("frameOutputs")
        self.gridLayout = QtWidgets.QGridLayout(self.frameOutputs)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.frameOutputs)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.totalTofBox = QtWidgets.QDoubleSpinBox(self.frameOutputs)
        self.totalTofBox.setStyleSheet("background-color: yellow")
        self.totalTofBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.totalTofBox.setDecimals(3)
        self.totalTofBox.setMaximum(99999999.99)
        self.totalTofBox.setObjectName("totalTofBox")
        self.gridLayout.addWidget(self.totalTofBox, 4, 1, 1, 1)
        self.centerCavityBox = QtWidgets.QDoubleSpinBox(self.frameOutputs)
        self.centerCavityBox.setAutoFillBackground(False)
        self.centerCavityBox.setStyleSheet("background-color: yellow")
        self.centerCavityBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.centerCavityBox.setDecimals(3)
        self.centerCavityBox.setMaximum(9999999999.99)
        self.centerCavityBox.setObjectName("centerCavityBox")
        self.gridLayout.addWidget(self.centerCavityBox, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frameOutputs)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frameOutputs)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frameOutputs)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.mcsDelayBox = QtWidgets.QDoubleSpinBox(self.frameOutputs)
        self.mcsDelayBox.setStyleSheet("background-color: yellow")
        self.mcsDelayBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.mcsDelayBox.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.mcsDelayBox.setDecimals(1)
        self.mcsDelayBox.setMaximum(99999999999.0)
        self.mcsDelayBox.setObjectName("mcsDelayBox")
        self.gridLayout.addWidget(self.mcsDelayBox, 5, 1, 1, 1)
        self.isepTrappingBox = QtWidgets.QDoubleSpinBox(self.frameOutputs)
        self.isepTrappingBox.setStyleSheet("background-color: yellow")
        self.isepTrappingBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.isepTrappingBox.setDecimals(3)
        self.isepTrappingBox.setMaximum(999999999.99)
        self.isepTrappingBox.setObjectName("isepTrappingBox")
        self.gridLayout.addWidget(self.isepTrappingBox, 3, 1, 1, 1)
        self.roundedCenterCavityBox = QtWidgets.QDoubleSpinBox(self.frameOutputs)
        self.roundedCenterCavityBox.setStyleSheet("background-color: lightgreen")
        self.roundedCenterCavityBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.roundedCenterCavityBox.setDecimals(3)
        self.roundedCenterCavityBox.setMaximum(100000000000.0)
        self.roundedCenterCavityBox.setObjectName("roundedCenterCavityBox")
        self.gridLayout.addWidget(self.roundedCenterCavityBox, 2, 2, 1, 1)
        self.roundedIsepTrappingBox = QtWidgets.QDoubleSpinBox(self.frameOutputs)
        self.roundedIsepTrappingBox.setStyleSheet("background-color: lightgreen")
        self.roundedIsepTrappingBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.roundedIsepTrappingBox.setDecimals(3)
        self.roundedIsepTrappingBox.setMaximum(999999999.99)
        self.roundedIsepTrappingBox.setObjectName("roundedIsepTrappingBox")
        self.gridLayout.addWidget(self.roundedIsepTrappingBox, 3, 2, 1, 1)
        self.roundedMcsDelayBox = QtWidgets.QDoubleSpinBox(self.frameOutputs)
        self.roundedMcsDelayBox.setStyleSheet("background-color: lightgreen")
        self.roundedMcsDelayBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.roundedMcsDelayBox.setDecimals(1)
        self.roundedMcsDelayBox.setMaximum(99999999999.0)
        self.roundedMcsDelayBox.setObjectName("roundedMcsDelayBox")
        self.gridLayout.addWidget(self.roundedMcsDelayBox, 5, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.frameOutputs)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 3)
        self.label_7 = QtWidgets.QLabel(self.frameOutputs)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 3)
        self.gridLayout_3.addWidget(self.frameOutputs, 0, 1, 1, 1)
        self.Table = QtWidgets.QTableWidget(self.centralwidget)
        self.Table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.Table.setAlternatingRowColors(True)
        self.Table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.Table.setColumnCount(11)
        self.Table.setObjectName("Table")
        self.Table.setRowCount(0)
        self.Table.horizontalHeader().setCascadingSectionResizes(False)
        self.Table.horizontalHeader().setDefaultSectionSize(100)
        self.Table.horizontalHeader().setMinimumSectionSize(45)
        self.Table.horizontalHeader().setSortIndicatorShown(True)
        self.Table.horizontalHeader().setStretchLastSection(True)
        self.Table.verticalHeader().setVisible(False)
        self.Table.verticalHeader().setDefaultSectionSize(20)
        self.Table.verticalHeader().setHighlightSections(False)
        self.Table.verticalHeader().setMinimumSectionSize(13)
        self.Table.verticalHeader().setStretchLastSection(False)
        self.gridLayout_3.addWidget(self.Table, 1, 0, 1, 4)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 2, 1, 1, 1)
        self.round_fact_ppg = QtWidgets.QDoubleSpinBox(self.frame)
        self.round_fact_ppg.setDecimals(1)
        self.round_fact_ppg.setMaximum(50000.0)
        self.round_fact_ppg.setProperty("value", 25.0)
        self.round_fact_ppg.setObjectName("round_fact_ppg")
        self.gridLayout_4.addWidget(self.round_fact_ppg, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 2, 2, 1, 1)
        self.round_fact_mcs = QtWidgets.QDoubleSpinBox(self.frame)
        self.round_fact_mcs.setDecimals(1)
        self.round_fact_mcs.setMaximum(50000.0)
        self.round_fact_mcs.setProperty("value", 1.0)
        self.round_fact_mcs.setObjectName("round_fact_mcs")
        self.gridLayout_4.addWidget(self.round_fact_mcs, 3, 2, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_4.addWidget(self.line_3, 1, 0, 1, 3)
        self.label_10 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 3)
        self.gridLayout_3.addWidget(self.frame, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1136, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNone = QtWidgets.QAction(MainWindow)
        self.actionNone.setObjectName("actionNone")
        self.actionCalibration = QtWidgets.QAction(MainWindow)
        self.actionCalibration.setObjectName("actionCalibration")
        self.actionAddExtra = QtWidgets.QAction(MainWindow)
        self.actionAddExtra.setObjectName("actionAddExtra")
        self.actionBuild_Spectrum = QtWidgets.QAction(MainWindow)
        self.actionBuild_Spectrum.setEnabled(False)
        self.actionBuild_Spectrum.setObjectName("actionBuild_Spectrum")
        self.menuFile.addAction(self.actionCalibration)
        self.menuFile.addAction(self.actionAddExtra)
        self.menuFile.addAction(self.actionBuild_Spectrum)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionNone)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.reqMassEdit, self.reqNRevsBox)
        MainWindow.setTabOrder(self.reqNRevsBox, self.centerCavityBox)
        MainWindow.setTabOrder(self.centerCavityBox, self.isepTrappingBox)
        MainWindow.setTabOrder(self.isepTrappingBox, self.totalTofBox)
        MainWindow.setTabOrder(self.totalTofBox, self.mcsDelayBox)
        MainWindow.setTabOrder(self.mcsDelayBox, self.tableShowButton)
        MainWindow.setTabOrder(self.tableShowButton, self.showSpectrum)
        MainWindow.setTabOrder(self.showSpectrum, self.Table)
        MainWindow.setTabOrder(self.Table, self.checkTofBox)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Isep Browser / Calibration"))
        self.checkTofBox.setSuffix(_translate("MainWindow", " ns"))
        self.label_6.setText(_translate("MainWindow", "Input Values"))
        self.reqMassEdit.setText(_translate("MainWindow", "85Rb"))
        self.label_5.setText(_translate("MainWindow", "Check ToF"))
        self.label.setText(_translate("MainWindow", "Requested Mass"))
        self.label_2.setText(_translate("MainWindow", "Requested Revs"))
        self.tableShowButton.setText(_translate("MainWindow", "Show me the Table"))
        self.tableShowButton.setShortcut(_translate("MainWindow", "Return"))
        self.showSpectrum.setText(_translate("MainWindow", "Show Spectrum"))
        self.label_4.setText(_translate("MainWindow", "Cavity Center"))
        self.totalTofBox.setSuffix(_translate("MainWindow", " us"))
        self.centerCavityBox.setSuffix(_translate("MainWindow", " us"))
        self.label_3.setText(_translate("MainWindow", "Isep Trapping"))
        self.label_9.setText(_translate("MainWindow", "MCS delay"))
        self.label_8.setText(_translate("MainWindow", "Total Time of Flight"))
        self.mcsDelayBox.setSuffix(_translate("MainWindow", " ns"))
        self.isepTrappingBox.setSuffix(_translate("MainWindow", " us"))
        self.roundedCenterCavityBox.setSuffix(_translate("MainWindow", " us"))
        self.roundedIsepTrappingBox.setSuffix(_translate("MainWindow", " us"))
        self.roundedMcsDelayBox.setSuffix(_translate("MainWindow", " ns"))
        self.label_7.setText(_translate("MainWindow", "Settings"))
        self.label_11.setText(_translate("MainWindow", "PPG"))
        self.round_fact_ppg.setSuffix(_translate("MainWindow", " ns"))
        self.label_12.setText(_translate("MainWindow", "MCS"))
        self.round_fact_mcs.setSuffix(_translate("MainWindow", " ns"))
        self.label_10.setText(_translate("MainWindow", "Rounding"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionNone.setText(_translate("MainWindow", "None!"))
        self.actionCalibration.setText(_translate("MainWindow", "Calibration"))
        self.actionCalibration.setShortcut(_translate("MainWindow", "Alt+C"))
        self.actionAddExtra.setText(_translate("MainWindow", "AddExtra"))
        self.actionAddExtra.setShortcut(_translate("MainWindow", "Alt+E"))
        self.actionBuild_Spectrum.setText(_translate("MainWindow", "Build Spectrum"))
        self.actionBuild_Spectrum.setShortcut(_translate("MainWindow", "Alt+B"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
