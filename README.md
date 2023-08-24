pyqtkeybind-PySide6 Binding
===========

Overview
--------

Global keybindings for PySide6, Only support Windows.

forked from [codito/pyqtkeybind](https://github.com/codito/pyqtkeybind)

Install and Sample
-------

See `sample/hotkey.py`


```

import sys

from qtpy.QtGui import QKeySequence
from qtpy import QtWidgets
from qtpy.QtCore import Qt, QAbstractNativeEventFilter, QAbstractEventDispatcher

from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    # Setup a global keyboard shortcut to print "Hello World" on pressing
    # the shortcut
    keybinder.init()
    unregistered = False


    def callback():
        print("hello world")


    key_command = QKeySequence(Qt.ControlModifier | Qt.Key_A)
    keybinder.register_hotkey(window.winId(), key_command, callback)

    # Install a native event filter to receive events from the OS
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    window.show()
    app.exec_()
    keybinder.unregister_hotkey(window.winId(), key_command)
```
