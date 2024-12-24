"""
Check:
разные ✅ одинаковые ✅

Форматы: .jpeg, .jpg, .png, .gif
Библиотека: Pillow
Установка: pip install Pillow

Библиотека: numpy
Установка:pip install numpy
"""
from PIL import Image
import numpy as np

def compare_images(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    if arr1.shape != arr2.shape:
        #print("Изображения имеют разные размеры.")
        return "Изображения имеют разные размеры."

    are_equal = np.array_equal(arr1, arr2)
    if are_equal:
        # print("Изображения идентичны!")
        return "Изображения идентичны!"
    else:
        # print("Изображения отличаются.")
        return "Изображения отличаются."