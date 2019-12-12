from image_thread import *
import sys
from pypylon import pylon, genicam
from PySide2 import QtWidgets

from ui import main

import os

os.environ["PYLON_CAMEMU"] = "1"


class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)

        self.frame_counter = 0

        self.printScreenOverlayButton.clicked.connect(self.save_print_screen)
        while True:
            try:
                self.camera = pylon.InstantCamera(
                    pylon.TlFactory.GetInstance().CreateFirstDevice())  # Иниициализируем первую доступную камеру
            except genicam.GenericException as e:
                print(f'{e}')
                time.sleep(3)
            else:
                break

        # Устанавливаем дефолтные значения для экспозиции
        self.exposure_slider.setMinimum(self.camera.ExposureTimeAbs.Min)
        self.exposure_slider.setMaximum(self.camera.ExposureTimeAbs.Max)
        self.exposure_slider.setSliderPosition(self.camera.ExposureTimeAbs.Min)
        # Устанавливаем дефолтные значения для усиления
        self.gain_slider.setMinimum(self.camera.GainRaw.Min)
        self.gain_slider.setMaximum(self.camera.GainRaw.Max)
        self.gain_slider.setSliderPosition(self.camera.GainRaw.Min)
        # Инициализируем конвертор формата изображения и сам формат
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.camera.Open()
        # TODO: вернуть!!! self.camera.BinningHorizontal = 2  # уменьшение размеров картинки по горизонтали
        # TODO: вернуть!!! self.camera.BinningVertical = 2  # уменьшение размеров картинки по вертикали
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        self.th = ImageThread(self.frame_counter, self.camera, self.exposure_slider, self.gain_slider, self.area_slider,
                              self.value_max_slider, self.value_min_slider, self.half_radio_button,
                              self.exponent_radio_button, self.ninty_percent_radio_button, self.converter, self.info_label, self.image_label)


        self.th.start()
        self.show()

    def save_print_screen(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qt_app = MyQtApp()

    app.exec_()
