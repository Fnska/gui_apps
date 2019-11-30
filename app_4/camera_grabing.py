from pypylon import pylon, genicam
import cv2
import time
# from functools import lru_cache
# from numba import jit
import os
os.environ["PYLON_CAMEMU"] = "1"


def nothing(*arg):
    """
    Заглушка для ползунков
    """
    pass


def calculation(grabResult, converter):
    # Доступ к данным с камеры в виде изображения
    image = converter.Convert(grabResult)
    img = image.GetArray()

    # Отслеживаем положение ползунков
    v_min = cv2.getTrackbarPos('v_min', 'Basler')
    v_max = cv2.getTrackbarPos('v_max', 'Basler')
    area = cv2.getTrackbarPos('area', 'Basler')

    # Конвертируем в GRAY и убираем шум (threshholding) в зависимости от положения ползунков
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshImgGray = cv2.inRange(imgGray, v_min, v_max)

    # Конвертирум в BGR, чтобы было синхронное изменение ползунков, картики и эллипсов (теряем качество цвета)
    imgBGR = cv2.cvtColor(threshImgGray, cv2.COLOR_GRAY2BGR)

    # Находим контуры по копии threshImgGray (в памяти)
    contours, hierarchy = cv2.findContours(threshImgGray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy, imgBGR, area


# @lru_cache()  # TODO: проверить
def main():
    try:
        camera = None
        # Подключаемся к первой доступной камере
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    except genicam.GenericException as e:
        print(f'{e}')
        time.sleep(1)
        main()
    else:
        # Открываем камеру
        camera.Open()

        """
        Binning обязаны  идти после camera.Open() и до camera.StartGrabbing()
        Доступные моды (Average, Sum) смотреть в документации docs.baslerweb.com
        1x1 = (1944, 2592), 2x2 = (972, 1296), 3x3 = (648, 864) , 4x4 = (486, 648) для acA2500-14gm
        """
        # TODO: вернуть!!! camera.BinningHorizontal = 2  # уменьшение размеров картинки по горизонтали
        # TODO: вернуть!!! camera.BinningVertical = 2  # уменьшение размеров картинки по вертикали

        # Собираем последовательно изображения (видео режим)
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter = pylon.ImageFormatConverter()

        # Конвертируем в bgr формат для opencv
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # Создаем окно и 2 ползунка
        cv2.namedWindow('Basler', cv2.WINDOW_NORMAL)
        cv2.createTrackbar('v_min', 'Basler', 0, 255, nothing)
        cv2.createTrackbar('v_max', 'Basler', 0, 255, nothing)
        cv2.createTrackbar('area', 'Basler', 10000, 2500 * 2000, nothing)
        cv2.createTrackbar('gain', 'Basler', camera.GainRaw.Min, camera.GainRaw.Max, nothing)  # для эмулятора 192 - 1023, для камеры 0-63
        cv2.createTrackbar('expos/35', 'Basler', int(camera.ExposureTimeAbs.Min / 35), int(camera.ExposureTimeAbs.Max / 35), nothing)  # для камеры 35 - 999985 с шагом 35, т.е. делим значения мин и мак на 35, чтобы был дискретный шаг и не было exeptions!

        cv2.setTrackbarPos('v_max', 'Basler', 255)  # Устанавливаем дефолтное значение = 255
        cv2.setTrackbarPos('area', 'Basler', 2500 * 100)  # Устанавливаем дефолтное значение = 250000
        cv2.setTrackbarPos('gain', 'Basler', int((camera.GainRaw.Min + camera.GainRaw.Max) / 2))
        cv2.setTrackbarPos('expos/35', 'Basler', int((camera.ExposureTimeAbs.Min / 35 + camera.ExposureTimeAbs.Max / 35) / 2))
        while camera.IsGrabbing():

            # start = time.time()

            # Получаем данные
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            camera.GainRaw = cv2.getTrackbarPos('gain', 'Basler')
            camera.ExposureTimeAbs.SetValue(cv2.getTrackbarPos('expos/35', 'Basler') * 35)

            if grabResult.GrabSucceeded():
                contours, hierarchy, imgBGR, area = calculation(grabResult, converter)
                # Для каждого контура, больше чем из 4-х точек аппроксимируем и рисуем эллипс (на основе контрастов).
                # Перебираем все найденные контуры с серой картинки в цикле
                for cnt in contours:
                    if len(cnt) > 4:
                        ellipse = cv2.fitEllipse(cnt)
                        areaOfEllipse = (int(ellipse[1][0]) * int(ellipse[1][1]))
                        if areaOfEllipse >= area:
                            # рисуем эллипс на восстановленном BGR изображении по координатам с серого изображения
                            cv2.ellipse(imgBGR, ellipse, (255, 0, 0), 5)
                            center = (int(ellipse[0][0]), int(ellipse[0][1]))
                            axes = (int(ellipse[1][0]), int(ellipse[1][1]))
                            cv2.circle(imgBGR, center, 5, (0, 0, 255), 2)
                            cv2.putText(imgBGR, f'{center}', (center[0] + 20, center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            cv2.putText(imgBGR, f'{axes[0]}', (center[0] - int(axes[0] / 4), center[1] - int(axes[0] / 4)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            cv2.putText(imgBGR, f'{axes[1]}', (center[0] + int(axes[1] / 4), center[1] - int(axes[1] / 4)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            grabResult.Release()

            # end = time.time()
            # print(f'{end-start}')

            cv2.imshow('Basler', imgBGR)
            k = cv2.waitKey(1)
            if k == 27:  # esc
                break
    finally:
        if camera is not None:
            # Освобождаем ресурсы
            camera.StopGrabbing()
            camera.Close()  # variative
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
