"""
Check:
разные ✅ одинаковые ✅

Форматы: .pdf
Библиотеки: PyPDF2, pdfplumber
Установка: pip install PyPDF2
"""

import PyPDF2
import difflib

def read_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return '\n'.join([page.extract_text() for page in reader.pages])

def compare_pdf_files(file1, file2):
    text1 = read_pdf(file1).splitlines()
    text2 = read_pdf(file2).splitlines()
    differ = difflib.unified_diff(text1, text2, fromfile=file1, tofile=file2)
    print('\n'.join(differ))
