from app import *

import cv2
from PySide2.QtCore import QThread
from PySide2.QtGui import QImage, QPixmap
from pypylon import pylon
import numpy as np


class ImageThread(QThread):
    def __init__(self, frame_counter, camera, exposure_slider, gain_slider, area_slider, value_max_slider,
                 value_min_slider, half_radio_button, exponent_radio_button, ninty_percent_radio_button, converter,
                 infoLabel, image_label):
        super(ImageThread, self).__init__()
        self.infoLabel = infoLabel
        self.converter = converter
        self.value_max_slider = value_max_slider
        self.area_slider = area_slider
        self.frame_counter = frame_counter
        self.value_min_slider = value_min_slider
        self.gain_slider = gain_slider
        self.exposure_slider = exposure_slider
        self.half_radio_button = half_radio_button
        self.exponent_radio_button = exponent_radio_button
        self.ninty_percent_radio_button = ninty_percent_radio_button
        self.camera = camera
        self.image_label = image_label

    def image_calculation(self, grab_result):
        image = self.converter.Convert(grab_result)
        img = image.GetArray()

        v_min = self.value_min_slider.value()
        v_max = self.value_max_slider.value()
        area = self.area_slider.value()

        self.frame_counter += 1
        self.infoLabel.setText(f'Frame: {self.frame_counter} \n'
                               f'Value min: {v_min} \n'
                               f'Value max: {v_max} \n'
                               f'Area: {area} \n'
                               f'Exposure: {self.exposure_slider.value()} \n'
                               f'Gain: {self.gain_slider.value()}')

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if (self.half_radio_button.isChecked()):
            self.value_min_slider.setSliderPosition(int(np.max(img_gray) / 2))
        if (self.exponent_radio_button.isChecked()):
            self.value_min_slider.setSliderPosition(int(np.max(img_gray) / np.e))
        if (self.ninty_percent_radio_button.isChecked()):
            self.value_min_slider.setSliderPosition(int(np.sum(img_gray) * 0.9))

        # TODO: сделать чек-баттон, позволяющую автоматически находить максимум как: np.max(img_gray), и устанавливать его на ползунок v_max

        thresh_img_gray = cv2.inRange(img_gray, v_min, v_max)
        img_gray_and_mask = cv2.bitwise_and(img_gray, img_gray, mask=thresh_img_gray)

        img_bgr = cv2.cvtColor(img_gray_and_mask, cv2.COLOR_GRAY2BGR)
        contours, hierarchy = cv2.findContours(img_gray_and_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy, img_bgr, area

    def display_video_stream(self):
        """
        Функция последовательной отрисовки изображения
        """
        grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        self.camera.GainRaw = self.gain_slider.value()
        self.camera.ExposureTimeAbs.SetValue(self.exposure_slider.value())

        if grab_result.GrabSucceeded():
            contours, hierarchy, img_bgr, area = self.image_calculation(grab_result)
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

    def run(self):
        while self.camera.IsGrabbing():
            self.display_video_stream()
