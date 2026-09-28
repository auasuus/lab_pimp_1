"""
ЛР 1.1 — Настройка окружения и базовый ввод-вывод
Вариант 5: Изображения + метаданные EXIF

Скрипт читает метаданные JPEG-файлов:
  - размер (ширина/высота, количество каналов)
  - EXIF-теги (дата съёмки, модель камеры и др., если они есть)

Запуск:
    python read_metadata.py photo.jpg
"""

import os
import sys


def read_image_metadata(file_path):
    """
    Читает базовые метаданные изображения (размер, каналы, глубина цвета).

    Используем OpenCV, т.к. он быстро и просто отдаёт матрицу пикселей
    и её форму (shape), из которой видно ширину, высоту и число каналов.

    :param file_path: путь к файлу изображения
    :return: словарь с базовыми метаданными
    """
    import cv2  # импортируем здесь, чтобы функцию можно было тестировать отдельно

    metadata = {}

    # cv2.imread возвращает numpy-массив пикселей, либо None, если файл
    # не найден / повреждён / формат не поддерживается
    img = cv2.imread(file_path)

    if img is None:
        # None — явный сигнал ошибки чтения, поэтому вместо того, чтобы
        # падать на следующей строке с невнятным AttributeError,
        # выбрасываем понятное исключение
        raise ValueError("Не удалось прочитать изображение (файл повреждён "
                          "или имеет неподдерживаемый формат)")

    # img.shape для цветного изображения имеет вид (высота, ширина, каналы)
    height, width = img.shape[0], img.shape[1]
    # если каналов нет в shape (двумерный массив) — значит изображение ч/б
    channels = img.shape[2] if len(img.shape) == 3 else 1

    metadata['ширина_px'] = width
    metadata['высота_px'] = height
    metadata['количество_каналов'] = channels
    # dtype показывает, сколько бит выделено на канал (uint8 -> 8 бит на канал)
    metadata['глубина_цвета'] = str(img.dtype)

    return metadata


def read_exif_metadata(file_path):
    """
    Читает EXIF-теги изображения (дата съёмки, модель камеры и т.д.).

    OpenCV не читает EXIF, поэтому для этой части используем Pillow (PIL) —
    она умеет доставать EXIF-словарь прямо из JPEG-файла.

    :param file_path: путь к файлу изображения
    :return: словарь с EXIF-тегами (человеко-читаемые ключи)
    """
    from PIL import Image
    from PIL import ExifTags

    exif_data = {}

    # Открываем изображение через Pillow. Если файл битый — здесь же упадёт
    # с исключением, которое мы обработаем в вызывающем коде (main).
    with Image.open(file_path) as img:
        raw_exif = img.getexif()

        if not raw_exif:
            # Пустой EXIF — не ошибка, а нормальная ситуация (например,
            # изображение сохранено без метаданных камеры)
            exif_data['EXIF'] = 'отсутствует'
            return exif_data

        # raw_exif — это словарь {числовой_код_тега: значение}.
        # ExifTags.TAGS переводит числовой код в читаемое имя (например,
        # 306 -> 'DateTime', 272 -> 'Model')
        for tag_id, value in raw_exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            exif_data[str(tag_name)] = value

    return exif_data


def main():
    """Основная функция: разбирает аргументы командной строки и запускает чтение."""

    # Проверяем, что пользователь передал имя файла аргументом
    if len(sys.argv) < 2:
        print("Использование: python read_metadata.py <файл.jpg>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Проверка существования файла — одна из требуемых обработок ошибок
    if not os.path.exists(file_path):
        print(f"Ошибка: файл не найден — {file_path}")
        sys.exit(1)

    # Проверка расширения — по заданию вариант 5 работает только с JPEG
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ('.jpg', '.jpeg'):
        print(f"Ошибка: ожидался JPEG-файл (.jpg/.jpeg), получено: {ext}")
        sys.exit(1)

    # Оборачиваем чтение в try/except, чтобы отловить повреждённые файлы
    try:
        size_metadata = read_image_metadata(file_path)
    except Exception as e:
        print(f"Ошибка при чтении изображения: {e}")
        sys.exit(1)

    try:
        exif_metadata = read_exif_metadata(file_path)
    except Exception as e:
        # EXIF может отсутствовать/быть повреждён — не прерываем программу,
        # просто сообщаем об этом
        print(f"Предупреждение: не удалось прочитать EXIF: {e}")
        exif_metadata = {}

    # Вывод результатов
    print(f"\nМетаданные изображения: {file_path}")
    print("-- Основные параметры --")
    for key, value in size_metadata.items():
        print(f"  {key}: {value}")

    print("-- EXIF-теги --")
    if exif_metadata:
        for key, value in exif_metadata.items():
            print(f"  {key}: {value}")
    else:
        print("  (EXIF-данные отсутствуют)")


if __name__ == '__main__':
    main()
