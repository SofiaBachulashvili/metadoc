from .botik import bot  # Импортируем объект бота
from telebot import types
from .compareFILES.compareFun import compare_files
from .commands import SAVE_FOLDER
import os
#from aiogram import types

#from convert_file import convertFile

# Функция временного хранения файла: сохранение -> (обработка) -> удаление




# Создание кнопок
@bot.message_handler(commands=['click'])
async def buttons(message):
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton('♻️Преобразовать♻️',callback_data='convert')
    markup.add(button1)

    button2 = types.InlineKeyboardButton('👀Сравнить👀', callback_data='compare')
    button3 = types.InlineKeyboardButton('🔤Переименовать🔤', callback_data='rename')
    markup.add(button2, button3)

    await bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


# Функции для кнопок
@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    # Получаем список всех файлов в папке
    files = [f for f in os.listdir(SAVE_FOLDER) if os.path.isfile(os.path.join(SAVE_FOLDER, f))]
    # Сортируем файлы по времени модификации и берем последние два
    files.sort(key=lambda x: os.path.getmtime(os.path.join(SAVE_FOLDER, x)), reverse=True)

    # Получаем адреса последних двух файлов
    if len(files) >= 2:
        file1 = os.path.join(SAVE_FOLDER, files[0])
        file2 = os.path.join(SAVE_FOLDER, files[1])

        if call.data == 'convert':
            text = 'Преобразованный файл\n'
            await bot.answer_callback_query(call.id)  # Подтверждение нажатия на кнопку
            await bot.send_message(call.message.chat.id, text)
            await bot.send_message()

        elif call.data == 'compare':
            text = 'Сравнение'
            await bot.answer_callback_query(call.id)
            await bot.send_message(call.message.chat.id, text)
            answer = compare_files(file1, file2)
            await bot.send_message(call.message.chat.id, answer)

        elif call.data == 'rename':
            text = 'Так гораздо лучше!\nПереименованный файл\n'
            await bot.answer_callback_query(call.id)
            await bot.send_message(call.message.chat.id, text)
    else:
        await bot.send_message(call.message.chat.id, 'Недостаточно файлов в папке.')