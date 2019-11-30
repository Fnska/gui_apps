# Графический интерфейс для программы обработки лазерных пучков

В данном репозитории представлен графический интерфейс, написанный на **Python**.

Основная программа лежит в папке **app_3** вместе с исполняемым файлом.

Новое дополнение в папке **app_4** - для динамического считывания информации с камер GIGe стандарта (например, Basler) и аппроксимации эллипсом.

## Возможности

* Отрисовка эллипса по точкам конкретной интесивности
* Пространственное представление пучка
* Выбор отдельных уровней интенсивности или наложение нескольких на исходное изображение

## В будущем

* Избавиться от фиксированных координат кадрирования изображения
* Обработка пучков более высоких мод
* Автоматическое распознавание моды

## Запуск

1. Запустите скомпилированный файл
2. Если хотите изменить область кадрирования
    1. Откройте approx_ellipse_img_V3.py
    2. Укажите интересующую область
    3. Перекомпилируйте проект: `pyinstaller app_gui.py`

## Лицензия

Смотрите раздел [License](https://github.com/Fnska/gui_apps/blob/master/LICENSE/)

## Содействие
1. Fork репозиторий!
2. Добавляйте изменения
3. Commit ваши изменения: `git commit -am 'Add some feature'`
4. Push изменения к вашей ветке: `git push origin master`
5. Отправляйте pull request :D
