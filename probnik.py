from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Тест')
        self.setGeometry(200, 200, 300, 300)

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())

        self.resize(pixmap.width(), pixmap.height())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    ex = App()
    ex.load_image('D:/Андрей/загрузки Chrome/Python/gui_apps/app_3/images')
    ex.show()

    sys.exit(app.exec_())
