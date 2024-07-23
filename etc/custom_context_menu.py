# coding=utf-8


from PyQt5 import QtCore, QtWidgets

import pyqtgraph as pg


class VboxCustomContextMenu(pg.ViewBox):
    """
    Class **VboxCustomContextMenu**

    Subclass of ViewBox to include custom functions
    within the pyqtgraph's standard context menu
    (that comes with right-click on the pyqtgraph ViewBox)

    =========================  ==============================================
    **Signals:**               **Description**
    =========================  ==============================================
    sigNewGaussFit(int)        USER requests a Gauss fit at ViewBox
    sigNewLinearFit(int)       USER requests a Linear fit at ViewBox
    sigCrossHair(int)          USER requests a drawing of Cross-Hairs
    sigRngFreeze(int)          USER requests the Range to freeze when updates
    sigSettings(int)           USER requests visualization of data parameters
    =========================  ==============================================

    """
    sigNoneFit = QtCore.pyqtSignal(int, name='sigNoneFit')
    sigGaussFit = QtCore.pyqtSignal(int, name='sigGaussFit')
    sigLinearFit = QtCore.pyqtSignal(int, name='sigLinearFit')
    sigCrossHair = QtCore.pyqtSignal(int, name='sigCrossHair')
    sigRngFreeze = QtCore.pyqtSignal(int, name='sigRngFreeze')
    sigSettings = QtCore.pyqtSignal(int, name='sigSettings')
    # sigDeltaTof = QtCore.pyqtSignal(int, name='sigDeltaTof')

    def __init__(self, parent=None, **kwargs) -> None:
        """
        Constructor of the VboxCustomContextMenu

        :param parent: default=None
        :param kwargs: All keyword argument that can be supplied to the ViewBox class of PyQtGraph

        """

        super(VboxCustomContextMenu, self).__init__(parent, **kwargs)

        # Set original plot context menu
        # Note: self.menu must not be None (this way works fine for plotWidgets,
        # but not for GraphicsWindow)
        self.menu = pg.graphicsItems.ViewBox.ViewBoxMenu.ViewBoxMenu(self)

        # Menu update property
        self.menuUpdate = True

    def getMenu(self, event=None):
        """
        Modify the menu. Called by the pyqtgraph.ViewBox raiseContextMenu() method.
        Arguments and Keywords matching the overloaded method of pyqtgraph class.

         .. note::
                Overwriting the ViewBox.py getMenu() function.

        """

        if self.menuUpdate is True:
            # # Modify contents of the original ViewBoxMenu
            # for action in self.menu.actions():
            #     # Modify the original Mouse Mode
            #     if "Mouse Mode" in action.text():
            #         # Change action labels
            #         for mouseAction in self.menu.leftMenu.actions():
            #             if "3 button" in mouseAction.text():
            #                 mouseAction.setText("CustomLabel1")
            #             elif "1 button" in mouseAction.text():
            #                 mouseAction.setText("CustomLabel2")

            # Add custom contents to menu
            self.addCustomToMenu()

            # Set menu update to false
            self.menuUpdate = False

        return self.menu

    def addCustomToMenu(self):
        """Add custom actions to the menu."""
        self.menu.addSeparator()
        self.fit_menu = self.menu.addMenu("Fit")

        self.actionNoneFit = QtWidgets.QAction("None", self.fit_menu)
        self.actionNoneFit.triggered.connect(self.sigNoneFit.emit)
        self.actionNoneFit.setCheckable(True)

        self.actionGaussFit = QtWidgets.QAction("Gauss", self.fit_menu)
        self.actionGaussFit.triggered.connect(self.sigGaussFit.emit)
        self.actionGaussFit.setCheckable(True)

        self.actionLinearFit = QtWidgets.QAction("Linear", self.fit_menu)
        self.actionLinearFit.triggered.connect(self.sigLinearFit.emit)
        self.actionLinearFit.setCheckable(True)

        # Create an action group - only one is active
        self.fitActionGroup = QtWidgets.QActionGroup(self.fit_menu)
        self.fitActionGroup.addAction(self.actionNoneFit)
        self.fitActionGroup.addAction(self.actionGaussFit)
        self.fitActionGroup.addAction(self.actionLinearFit)
        self.actionNoneFit.setChecked(True)

        # Add to fit menu is required
        self.fit_menu.addAction(self.actionNoneFit)
        self.fit_menu.addAction(self.actionGaussFit)
        self.fit_menu.addAction(self.actionLinearFit)

        # Create an action
        self.actionCrHr = QtWidgets.QAction("Crosshair", self.menu)
        self.actionCrHr.triggered.connect(self.sigCrossHair.emit)
        self.actionCrHr.setCheckable(True)
        # Add to main menu
        self.menu.addAction(self.actionCrHr)

        # Create an action
        self.rngUpdLoad = QtWidgets.QAction("Range Freeze?", self.menu)
        self.rngUpdLoad.triggered.connect(self.sigRngFreeze.emit)
        self.rngUpdLoad.setCheckable(True)
        # Add to main menu
        self.menu.addAction(self.rngUpdLoad)

        # Create an action
        self.settings = QtWidgets.QAction("File Settings", self.menu)
        self.settings.triggered.connect(self.sigSettings.emit)
        # self.settings.setCheckable(True)
        # Add to main menu
        self.menu.addAction(self.settings)

        # # Create an action
        # self.delta_tof = QtWidgets.QAction("Show Delta to IOI", self.menu)
        # self.delta_tof.triggered.connect(self.sigDeltaTof.emit)
        # self.delta_tof.setCheckable(True)
        # # Add to main menu
        # self.menu.addAction(self.delta_tof)