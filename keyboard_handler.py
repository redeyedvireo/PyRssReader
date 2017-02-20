from PyQt5 import QtCore


class KeyboardHandler(QtCore.QObject):
    nextFeedItemSignal = QtCore.pyqtSignal()
    previousFeedItemSignal = QtCore.pyqtSignal()
    nextFeedSignal = QtCore.pyqtSignal()
    previousFeedSignal = QtCore.pyqtSignal()
    minimizeApplicationSignal = QtCore.pyqtSignal()

    # The key table maps keypresses to signals
    keyTable = [ { 'signal': 'nextFeedItemSignal', 'keys': [QtCore.Qt.Key_Plus, QtCore.Qt.Key_6] },
                 { 'signal': 'previousFeedItemSignal', 'keys': [QtCore.Qt.Key_Minus, QtCore.Qt.Key_4] },
                 { 'signal': 'previousFeedSignal', 'keys': [QtCore.Qt.Key_8] },
                 { 'signal': 'nextFeedSignal', 'keys': [QtCore.Qt.Key_2] },
                 { 'signal': 'minimizeApplicationSignal', 'keys': [QtCore.Qt.Key_5] }
                 ]

    def __init__(self, parent):
        super(KeyboardHandler, self).__init__(parent)

    def handleKey(self, keyCode):
        """ Emits an appropriate signal, if the keyCode maps to an action.
            Returns True if the keyCode was mapped (and a signal sent); False if not. """

        for keyAssignment in self.keyTable:
            if keyCode in keyAssignment['keys']:
                signal = getattr(self, keyAssignment['signal'])
                signal.emit()
                return True
        return False
