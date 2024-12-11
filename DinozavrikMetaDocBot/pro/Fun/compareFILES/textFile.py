"""
Форматы: .txt, .md, .py, .cpp, .cs
Библиотека: Стандартные функции чтения и difflib
"""
"""
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

