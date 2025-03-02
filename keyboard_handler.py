from PySide6 import QtCore


class KeyboardHandler(QtCore.QObject):
    nextFeedItemSignal = QtCore.Signal()
    previousFeedItemSignal = QtCore.Signal()
    nextFeedSignal = QtCore.Signal()
    previousFeedSignal = QtCore.Signal()
    minimizeApplicationSignal = QtCore.Signal()

    # The key table maps keypresses to signals
    keyTable = [ { 'signal': 'nextFeedItemSignal', 'keys': [QtCore.Qt.Key.Key_Plus, QtCore.Qt.Key.Key_6] },
                 { 'signal': 'previousFeedItemSignal', 'keys': [QtCore.Qt.Key.Key_Minus, QtCore.Qt.Key.Key_4] },
                 { 'signal': 'previousFeedSignal', 'keys': [QtCore.Qt.Key.Key_8] },
                 { 'signal': 'nextFeedSignal', 'keys': [QtCore.Qt.Key.Key_2] },
                 { 'signal': 'minimizeApplicationSignal', 'keys': [QtCore.Qt.Key.Key_5] }
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
