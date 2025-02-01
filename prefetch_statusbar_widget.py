from PySide6 import QtCore, QtGui, QtWidgets


class PrefetchStatusbarWidget(QtWidgets.QLabel):
    def __init__(self, parent):
        super(PrefetchStatusbarWidget, self).__init__(parent)

    @QtCore.Slot()
    def prefetchOn(self):
        """ Called to turn the prefetch indicator on. """
        self.setText("Prefetching images...")

    @QtCore.Slot()
    def prefetchOff(self):
        """ Called to turn the prefetch indicator off. """
        self.setText("")
