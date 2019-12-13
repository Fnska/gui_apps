# import os
import sys
import time

from PySide2 import QtWidgets
from pypylon import pylon, genicam
import cv2
import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import QThread
from PySide2.QtGui import QImage, QPixmap


from ui import main

# os.environ["PYLON_CAMEMU"] = "1"


class ImageThread(QThread):
    def __init__(self, camera, exposure_slider, gain_slider, area_slider, value_max_slider,
                 value_min_slider, half_radio_button, exponent_radio_button, ninety_percent_radio_button, converter,
                 info_label, image_label):
        """
        Инициализируем тред с переданными в него параметры для обработки без блокировки главного окна
        """
        super(ImageThread, self).__init__()
        self.info_label = info_label
        self.converter = converter
        self.value_max_slider = value_max_slider
        self.area_slider = area_slider
        self.frame_counter = 0
        self.value_min_slider = value_min_slider
        self.gain_slider = gain_slider
        self.exposure_slider = exposure_slider
        self.half_radio_button = half_radio_button
        self.exponent_radio_button = exponent_radio_button
        self.ninety_percent_radio_button = ninety_percent_radio_button
        self.camera = camera
        self.image_label = image_label

    def image_calculation(self, grab_result):
        """
        Функция нахождения контуров и вырезания по маске изображения с обрезанной интенсивностью
        :param grab_result: Результат полученный с камеры
        :return: список контуров, иерархия контуров, обработанное изображение в BGR, площадь со слайдера
        """

        image = self.converter.Convert(grab_result)  # Конвертируем наши полученные данные в изображение BGR
        img = image.GetArray()  # Получаем изображение в виде массива

        # Считываем значения со слайдеров
        v_min = self.value_min_slider.value()
        v_max = self.value_max_slider.value()
        area = self.area_slider.value()

        # Прибавляем 1 фрейм обработки
        self.frame_counter += 1

        # Печатаем значения наших слайдеров на лейбл информации
        self.info_label.setText(f'Frame: {self.frame_counter} \n'
                                f'Value min: {v_min} \n'
                                f'Value max: {v_max} \n'
                                f'Area: {area} \n'
                                f'Exposure: {self.exposure_slider.value()} \n'
                                f'Gain: {self.gain_slider.value()}')

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Ковертируем BGR в GRAY

        # Проверяем на чек радио-кнопки
        if (self.half_radio_button.isChecked()):
            self.value_min_slider.setSliderPosition(int(np.max(img_gray) / 2))
        if (self.exponent_radio_button.isChecked()):
            self.value_min_slider.setSliderPosition(int(np.max(img_gray) / np.e))
        if (self.ninety_percent_radio_button.isChecked()):
            self.value_min_slider.setSliderPosition(int(np.sum(img_gray) * 0.9))

        # TODO: сделать чек-баттон, позволяющую автоматически находить максимум как: np.max(img_gray), и устанавливать его на ползунок v_max

        # Выделяем маску по значениям фильтра интенсивности и закрашиваем ее полностью в белый (255)
        thresh_img_gray = cv2.inRange(img_gray, v_min, v_max)

        # Вставляем на место маски исходное серое изображение, остальное обращаем в черный(0)
        img_gray_and_mask = cv2.bitwise_and(img_gray, img_gray, mask=thresh_img_gray)

        # Конвертируем GRAY в BGR
        img_bgr = cv2.cvtColor(img_gray_and_mask, cv2.COLOR_GRAY2BGR)

        # Находим контуры
        contours, hierarchy = cv2.findContours(img_gray_and_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy, img_bgr, area

    def display_video_stream(self):
        """
        Функция последовательной отрисовки изображения (видео)
        """
        grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)  # Получаем данные с камеры

        self.camera.GainRaw = self.gain_slider.value()  # Устанавливаем Gain камеры на значение со слайдера
        self.camera.ExposureTimeAbs.SetValue(
            self.exposure_slider.value())  # Устанавливаем ExposureTimeAbs камеры на значение со слайдера

        if grab_result.GrabSucceeded():
            contours, hierarchy, img_bgr, area = self.image_calculation(grab_result)
            for cnt in contours:
                """
                Для каждого контура, больше чем из 4-х точек аппроксимируем и рисуем эллипс (на основе контрастов).
                Перебираем все найденные контуры с серой картинки в цикле.
                Рисуем на BGR картинке линии и текст.
                """
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

        grab_result.Release()  # Очищаем результат

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # Конвертируем BGR в RGB

        # Конвертируем RGB в Qt изображение
        img_qt = QImage(img_rgb, img_rgb.shape[1], img_rgb.shape[0], img_rgb.strides[0], QImage.Format_RGB888)

        # Создаем QPixmap из Qt изображения и скейлим его размер под размер лейбла отображения, сохраняя пропорции
        pixmap = QPixmap.fromImage(img_qt).scaled(QtCore.QSize(self.image_label.width(), self.image_label.height()),
                                                  QtCore.Qt.KeepAspectRatio)
        # Обновляем лейбл изображения
        self.image_label.setPixmap(pixmap)

    def run(self):
        """
        Данный метод запустится при старке треда.
        Будет пробегать цикл получения данных и их отрисовки до тех пор, пока камера снимает
        """
        while self.camera.IsGrabbing():
            self.display_video_stream()


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

        # Устанавливаем дефолтные значения для ExposureTimeAbs (экспозиции) в слайдер
        self.exposure_slider.setMinimum(self.camera.ExposureTimeAbs.Min)
        self.exposure_slider.setMaximum(self.camera.ExposureTimeAbs.Max)
        self.exposure_slider.setSliderPosition(self.camera.ExposureTimeAbs.Min)

        # Устанавливаем дефолтные значения для Gain (усиления) в слайдер
        self.gain_slider.setMinimum(self.camera.GainRaw.Min)
        self.gain_slider.setMaximum(self.camera.GainRaw.Max)
        self.gain_slider.setSliderPosition(self.camera.GainRaw.Min)

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
        # TODO: вернуть!!! self.camera.BinningHorizontal = 2  # уменьшение размеров картинки по горизонтали
        # TODO: вернуть!!! self.camera.BinningVertical = 2  # уменьшение размеров картинки по вертикали

        self.camera.StartGrabbing(
            pylon.GrabStrategy_LatestImageOnly)  # Начинаем последовательно собирать изображения (видео режим)

        # Передаем в отдельный тред камеру, слайдеры и радио-кнопки для обработки без блокировки главного окна
        self.th = ImageThread(self.camera, self.exposure_slider, self.gain_slider,
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
