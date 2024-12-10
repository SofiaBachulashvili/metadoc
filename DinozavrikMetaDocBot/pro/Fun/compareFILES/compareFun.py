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
        Er = 'Неподдерживаемый формат файла'
        return Er


def compare_files(file1, file2):
    str = 'No compare yet'
    try:
        if file1.endswith(('.jpeg', '.jpg', '.png', '.gif')) and file2.endswith(('.jpeg', '.jpg', '.png', '.gif')):
            are_equal = compare_images(file1, file2)
            if are_equal:
                str = 'Изображения одинаковые'
                return str
            else:
                str = 'Изображения разные'
                return str
        else:
            lines1 = read_file(file1)
            lines2 = read_file(file2)
            differ = list(difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2))

            if not differ:
                str = 'Файлы одинаковые'
                return str
            else:
                str = 'Файлы разные'
                return str
    except Exception as e:
        e = '[!] Ошибка '
        return e
        #print(f"Ошибка: {e}")

# Пример использования

#compare_images('C:/Users/Sofia/Pictures/Saved Pictures/D.jpg', 'C:/Users/Sofia/Pictures/Saved Pictures/D2.jpg')
#compare_files('C:/Users/Sofia/Desktop/(2).txt', 'C:/Users/Sofia/Desktop/5st.txt')