import difflib
from .textFile import read_text_file, compare_text_files      # Импортируем функции работы с текстовыми файлами
from .docxFile import read_docx, compare_docx_files          # Импортируем функции работы с .docx файлами
from .pdfFile import read_pdf, compare_pdf_files              # Импортируем функции работы с .pdf файлами
from .pictureFile import compare_images                        # Импортируем функцию сравнения изображений

def read_file(file_path):
    if file_path.endswith(('.txt', '.md', '.py', '.cpp', '.cs')):
        return read_text_file(file_path)
    elif file_path.endswith('.docx'):
        return read_docx(file_path).splitlines()
    elif file_path.endswith('.pdf'):
        return read_pdf(file_path).splitlines()
    elif file_path.endswith(('.jpeg', '.jpg', '.png', '.gif')):
        return None  # Обработка изображений отдельно
    else:
        #raise ValueError("Неподдерживаемый формат файла")
        return 'Неподдерживаемый формат файла'


def compare_files(file1, file2):
    try:
        # Проверка формата файлов
        format1 = file1.split('.')[-1]
        format2 = file2.split('.')[-1]

        if format1 != format2:
            return f'Файлы разного формата: {format1} и {format2}. Невозможно провести сравнение.'

        if file1.endswith(('.jpeg', '.jpg', '.png', '.gif')) and file2.endswith(('.jpeg', '.jpg', '.png', '.gif')):
            are_equal = compare_images(file1, file2)
            if are_equal:
                return 'Изображения одинаковые 🖼️🖼️'
            else:
                return 'Изображения разные ️⬅️🖼️➡️'
        else:
            lines1 = read_file(file1)
            lines2 = read_file(file2)
            differ = list(difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2))

            if not differ:
                return 'Файлы одинаковые 📁📁'
            else:
                return 'Файлы разные ️⬅️📁➡️'
    except Exception as e:
        return f'[!] Ошибка: {e}'

#compare_images('C:/Users/Sofia/Pictures/Saved Pictures/D.jpg', 'C:/Users/Sofia/Pictures/Saved Pictures/D2.jpg')
#compare_files('C:/Users/Sofia/Desktop/(2).txt', 'C:/Users/Sofia/Desktop/5st.txt')