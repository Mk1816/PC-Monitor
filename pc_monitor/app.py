import sys

from PyQt6.QtWidgets import QApplication

from pc_monitor.ui.main_window import MainWindow


def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("PC Monitor")
    window = MainWindow()
    window.show()
    return app.exec()
