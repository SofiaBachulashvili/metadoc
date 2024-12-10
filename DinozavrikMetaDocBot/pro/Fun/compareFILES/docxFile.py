"""
Форматы: .doc, .docx
Библиотека: python-docx
Установка: pip install python-docx
"""
import difflib
from docx import Document


def read_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def compare_docx_files(file1, file2):
    text1 = read_docx(file1).splitlines()
    text2 = read_docx(file2).splitlines()
    differ = difflib.unified_diff(text1, text2, fromfile=file1, tofile=file2)
    print('\n'.join(differ))
