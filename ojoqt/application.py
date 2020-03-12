import sys
import traceback
import typing

from PyQt5.QtWidgets import QApplication, QMessageBox

import ojoqt


class BaseApplication(QApplication):
    main_window_cls = None

    def __init__(self, argv: typing.List[str]):
        super().__init__(argv)
        self.main_window = None  # type: ojoqt.BaseMainWindow

    def callback_catch(self, exc: str):
        print(exc, file=sys.stderr)
        QMessageBox.warning(self.main_window, 'Error', exc)

    def hook_exception(self):
        def boom(type_, value, tb):
            import traceback
            exc = ''.join(traceback.format_exception(type_, value, tb))
            self.callback_catch(exc)

        sys.excepthook = boom

    def run(self):
        try:
            self.hook_exception()
            self.main_window = self.main_window_cls(self)
            self.main_window.show()
            return self.exec_()
        except:
            exc = traceback.format_exc()
            self.callback_catch(exc)
            return 1
