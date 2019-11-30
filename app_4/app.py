import os
import sys
import time

import cv2
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer, QThread, QEventLoop
from PySide2.QtGui import QPixmap, QImage
from pypylon import pylon, genicam

from ui import main

# os.environ["PYLON_CAMEMU"] = "1"
count = 0


class MyThread(QThread):

    def calculation(self, grab_result):
        image = self.converter.Convert(grab_result)
        img = image.GetArray()

        v_min = self.value_min_slider.value()
        v_max = self.value_max_slider.value()
        area = self.area_slider.value()

        global count
        count += 1
        self.infoLabel.setText(f'Frame: {count} \n'
                               f'Value min: {v_min} \n'
                               f'Value max: {v_max} \n'
                               f'Area: {area} \n'
                               f'Exposure/35: {self.exposure_slider.value()} \n'
                               f'Gain: {self.gain_slider.value()}')

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh_img_gray = cv2.inRange(img_gray, v_min, v_max)  # TODO: не HardCode!

        img_bgr = cv2.cvtColor(thresh_img_gray, cv2.COLOR_GRAY2BGR)

        contours, hierarchy = cv2.findContours(thresh_img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy, img_bgr, area

    def display_video_stream(self):
        """
        Функция последовательной отрисовки изображения
        """
        grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
            contours, hierarchy, img_bgr, area = self.calculation(grab_result)
            for cnt in contours:
                if len(cnt) > 4:
                    ellipse = cv2.fitEllipse(cnt)
                    area_of_ellipse = (int(ellipse[1][0]) * int(ellipse[1][1]))
                    if area_of_ellipse >= area:
                        center = (int(ellipse[0][0]), int(ellipse[0][1]))
                        axes = (int(ellipse[1][0]), int(ellipse[1][1]))

                        cv2.ellipse(img_bgr, ellipse, (255, 0, 0), 5)
                        cv2.circle(img_bgr, center, 5, (0, 0, 255), 2)

                        cv2.putText(img_bgr, f'{center}', (center[0] + 20, center[1] - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 2)
                        cv2.putText(img_bgr, f'{axes[0]}',
                                    (center[0] - int(axes[0] / 4), center[1] - int(axes[0] / 4)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.putText(img_bgr, f'{axes[1]}',
                                    (center[0] + int(axes[1] / 4), center[1] - int(axes[1] / 4)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        grab_result.Release()

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_qt = QImage(img_rgb, img_rgb.shape[1], img_rgb.shape[0], img_rgb.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(img_qt))

    def __init__(self, info_label, image_label, value_min_slider, value_max_slider, area_slider, exposure_slider,
                 gain_slider, *args,
                 **kwargs):
        QThread.__init__(self, *args, **kwargs)

        # Инициализируем слайдеры для треда-обработчика
        self.value_min_slider = value_min_slider
        self.value_max_slider = value_max_slider
        self.area_slider = area_slider
        self.exposure_slider = exposure_slider
        self.gain_slider = gain_slider

        # Инициализируем лейблы для треда-обработчика
        self.infoLabel = info_label
        self.image_label = image_label

        self.args = args
        self.kwargs = kwargs

        self.camera = None

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
        self.exposure_slider.setMinimum(self.camera.ExposureTimeAbs.Min / 35)
        self.exposure_slider.setMaximum(self.camera.ExposureTimeAbs.Max / 35)
        self.exposure_slider.setSliderPosition(
            int((self.camera.ExposureTimeAbs.Min / 35 + self.camera.ExposureTimeAbs.Max / 35) / 2))

        # Устанавливаем дефолтные значения для усиления
        self.gain_slider.setMinimum(self.camera.GainRaw.Min)
        self.gain_slider.setMaximum(self.camera.GainRaw.Max)
        self.gain_slider.setSliderPosition(int((self.camera.GainRaw.Min + self.camera.GainRaw.Max) / 2))

        # Инициализируем конвертор формата изображения и сам формат
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        self.camera.Open()
        # TODO: вернуть!!! self.camera.BinningHorizontal = 2  # уменьшение размеров картинки по горизонтали
        # TODO: вернуть!!! self.camera.BinningVertical = 2  # уменьшение размеров картинки по вертикали
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        # Устанавливаем таймер обновления картинки
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.display_video_stream)

    def run(self):
        self.timer.start(100)
        loop = QEventLoop()
        loop.exec_()


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
    th = MyThread(qt_app.info_label, qt_app.image_label, qt_app.value_min_slider, qt_app.value_max_slider,
                  qt_app.area_slider, qt_app.exposure_slider, qt_app.gain_slider)

    th.start()
    qt_app.show()
    app.exec_()
