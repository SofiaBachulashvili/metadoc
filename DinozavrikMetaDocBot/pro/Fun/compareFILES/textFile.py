"""
Check ✅
Форматы:
    .txt, разные ✅ одинаковые✅
    .md, разные ✅ одинаковые ✅
    .py, разные ✅ одинаковые ✅
    .cpp, разные ✅ одинаковые ✅
    .cs разные ✅ одинаковые ✅
Библиотека: Стандартные функции чтения и difflib
"""
import difflib  # Импортируем модуль для сравнения текстов

def read_text_file(file_path):
    try:
        # Проверка формата файла, получаем расширение
        format = file_path.split('.')[-1]
        if format == 'md':  # Если файл в формате Markdown
            try:
                # Пытаемся открыть файл с кодировкой utf-8
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.readlines()  # Читаем и возвращаем строки файла
            except UnicodeDecodeError:  # Если возникает ошибка кодировки
                # Открываем файл с кодировкой latin-1
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.readlines()  # Читаем и возвращаем строки файла
        else:
            # Если формат не Markdown, открываем файл с используемой по умолчанию кодировкой
            with open(file_path, 'r') as f:
                return f.readlines()  # Читаем и возвращаем строки файла
    except Exception as e:
        return f'[!] Ошибка: {e}'  # Возвращаем сообщение об ошибке

def compare_text_files(file1, file2):
    # Читаем строки из первого файла
    lines1 = read_text_file(file1)
    # Читаем строки из второго файла
    lines2 = read_text_file(file2)
    # Сравниваем файлы и получаем различия
    differ = difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2)
    # Выводим различия на экран
    print('\n'.join(differ))


"""
# txt
import difflib

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

def compare_text_files(file1, file2):
    lines1 = read_text_file(file1)
    lines2 = read_text_file(file2)
    differ = difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2)
    print('\n'.join(differ))

"""
"""
# Работает с .md
import difflib

def read_text_file(file_path):
    # Пробуем открытие с разными кодировками
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.readlines()

def compare_text_files(file1, file2):
    lines1 = read_text_file(file1)
    lines2 = read_text_file(file2)
    differ = difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2)
    print('\n'.join(differ))
"""