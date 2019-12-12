import sys

from PySide2 import QtWidgets

from ui import main
from v2.ImageThread import ImageThread


class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.printScreenOverlayButton.clicked.connect(self.save_print_screen)

    def save_print_screen(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qt_app = MyQtApp()
    th = ImageThread()

    th.start()
    qt_app.show()
    app.exec_()
