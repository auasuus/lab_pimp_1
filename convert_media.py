"""
ЛР 1.1 — Настройка окружения и базовый ввод-вывод
Вариант 5: Изображения + метаданные EXIF

Скрипт конвертирует изображение JPEG -> PNG с помощью FFmpeg.

Запуск:
    python convert_media.py photo.jpg photo.png
"""

import subprocess
import shutil
import sys
import os


def check_ffmpeg():
    """
    Проверяет, установлен ли FFmpeg и виден ли он в PATH.

    shutil.which('ffmpeg') ищет исполняемый файл ffmpeg во всех папках,
    перечисленных в переменной окружения PATH. Если ничего не найдено,
    возвращается None.
    """
    if shutil.which('ffmpeg') is None:
        print("Ошибка: FFmpeg не найден в системе.")
        print("Установите FFmpeg и добавьте его в PATH, затем повторите попытку.")
        sys.exit(1)
    # если дошли сюда — FFmpeg найден, можно продолжать


def convert_file(input_path, output_path):
    """
    Конвертирует изображение из JPEG в PNG при помощи FFmpeg.

    :param input_path: путь к исходному .jpg/.jpeg файлу
    :param output_path: путь, куда сохранить .png файл
    :return: True при успешной конвертации, False при ошибке
    """
    # Проверка существования входного файла — типичная ошибка, которую
    # нужно обработать до запуска внешней программы
    if not os.path.exists(input_path):
        print(f"Ошибка: входной файл не найден — {input_path}")
        return False

    # Проверка расширения входного файла под вариант 5 (JPEG -> PNG)
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in ('.jpg', '.jpeg'):
        print(f"Ошибка: ожидался JPEG-файл на входе, получено: {ext}")
        return False

    # Формируем команду для FFmpeg:
    #   -i input_path   -- входной файл
    #   -y               -- перезаписать выходной файл без вопроса, если он уже есть
    #   output_path      -- выходной файл (по расширению .png FFmpeg сам поймёт формат)
    cmd = ['ffmpeg', '-i', input_path, '-y', output_path]

    try:
        # capture_output=True перехватывает stdout/stderr, чтобы можно было
        # показать сообщение об ошибке, а не "залить" консоль логами ffmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        # На случай, если ffmpeg пропал между check_ffmpeg() и этим вызовом
        print("Ошибка: не удалось запустить FFmpeg.")
        return False
    except Exception as e:
        print(f"Непредвиденная ошибка при запуске FFmpeg: {e}")
        return False

    # FFmpeg возвращает код 0 при успехе и ненулевой код при ошибке
    # (например, битый входной файл, нет прав на запись и т.д.)
    if result.returncode != 0:
        # Показываем только хвост лога ffmpeg, чтобы не засорять вывод
        print("Ошибка конвертации, вывод FFmpeg:")
        print(result.stderr[-500:])
        return False

    return True


def main():
    """Основная функция: разбирает аргументы и запускает конвертацию."""

    if len(sys.argv) < 3:
        print("Использование: python convert_media.py <входной.jpg> <выходной.png>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Шаг 1 — проверяем, что FFmpeg вообще установлен
    check_ffmpeg()

    # Шаг 2 — выполняем конвертацию
    success = convert_file(input_path, output_path)

    # Шаг 3 — сообщаем результат пользователю
    if success:
        print(f"Конвертация завершена успешно: {input_path} -> {output_path}")
    else:
        print("Конвертация не выполнена.")
        sys.exit(1)


if __name__ == '__main__':
    main()
