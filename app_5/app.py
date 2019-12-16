# import os
import sys
import time

from PySide2 import QtWidgets
from pypylon import pylon, genicam

import image_thread
from ui import main

# os.environ["PYLON_CAMEMU"] = "1"


class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)

        self.printScreenOverlayButton.clicked.connect(self.save_print_screen_overlay)
        self.printScreenButton.clicked.connect(self.save_print_screen)

        while True:  # Ищем камеру до тех пора, пока не появится первая доступная
            try:
                self.camera = pylon.InstantCamera(
                    pylon.TlFactory.GetInstance().CreateFirstDevice())  # Иниициализируем первую доступную камеру
            except genicam.GenericException as e:
                print(f'{e}')
                time.sleep(3)
            else:
                break



        # Инициализируем конвертор формата изображения и сам формат
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        self.camera.Open()  # Открываем камеру

        """
        Binning обязаны  идти после camera.Open() и до camera.StartGrabbing()
        Доступные моды (Average, Sum) смотреть в документации docs.baslerweb.com
        1x1 = (1944, 2592), 2x2 = (972, 1296), 3x3 = (648, 864) , 4x4 = (486, 648) для acA2500-14gm
        """
        self.camera.BinningHorizontal = 2  # TODO: вернуть!!! уменьшение размеров картинки по горизонтали
        self.camera.BinningVertical = 2  # TODO: вернуть!!! уменьшение размеров картинки по вертикали

        """
        Устанавливаем дефолтные значения для ExposureTimeAbs (экспозиции) в слайдер
        ExposureTimeAbs.Min и GainRaw.Min обязаны идти после camera.Open()
        """
        self.exposure_slider.setMinimum(self.camera.ExposureTimeAbs.Min)
        self.exposure_slider.setMaximum(self.camera.ExposureTimeAbs.Max)
        self.exposure_slider.setSliderPosition(self.camera.ExposureTimeAbs.Min)

        # Устанавливаем дефолтные значения для Gain (усиления) в слайдер
        self.gain_slider.setMinimum(self.camera.GainRaw.Min)
        self.gain_slider.setMaximum(self.camera.GainRaw.Max)
        self.gain_slider.setSliderPosition(self.camera.GainRaw.Min)

        self.camera.StartGrabbing(
            pylon.GrabStrategy_LatestImageOnly)  # Начинаем последовательно собирать изображения (видео режим)

        # Передаем в отдельный тред камеру, слайдеры и радио-кнопки для обработки без блокировки главного окна
        self.th = image_thread.ImageThread(self.camera, self.exposure_slider, self.gain_slider,
                                           self.area_slider,
                                           self.value_max_slider, self.value_min_slider, self.half_radio_button,
                                           self.exponent_radio_button, self.ninety_percent_radio_button, self.converter,
                                           self.info_label, self.image_label)

        self.th.start()  # Запускаем тред
        self.show()  # Отображаем главное окно

    def save_print_screen_overlay(self):
        """
        Функция скриншота с оверлеем
        """
        pass

    def save_print_screen(self):
        """
        Функция скриншота без оверлея
        """
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qt_app = MyQtApp()  # Стартуем приложение

    app.exec_()
