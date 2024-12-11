from telebot import types
import os
import shutil

from .botik import bot  # Импортируем объект бота, используя относительный путь .botik
from .compareFILES.compareFun import compare_files





# Обработчик для команд /start, /Hello, /Hola
@bot.message_handler(commands=['start', 'Hello', 'Hola'])
async def start_command(message):
    await bot.send_message(message.chat.id,
                           f"Hola, {message.from_user.first_name}!\nI am dinozavrik Metadoc\nLet's be friends.🌸\nI am learning to work with files.")


@bot.message_handler(commands=['help'])  # Обрабатываем команду /help
async def help_command(message):
    # Определяем список доступных команд
    commands_list = [
        '/start - Начало общения с ботом',
        '/help - Получить список доступных команд',
        '/handle_document - Переименовать документ',
        '/save_file_for_work - Сохранить файл для обработки',
        '/click - Выбор действия с файлом',
        '/Dinozavrik_Secret_Diary - Узнать историю Dinozavrika'
    ]

    # Формируем сообщение со списком команд
    commands_text = "<u>Available Commands:</u>\n" + "\n".join(commands_list)

    # Отправляем сообщение пользователю с командами
    await bot.send_message(message.chat.id, commands_text, parse_mode='html')
    """
        parse_mode = 'html'
        <b> </b> - жирный
        <em> </em> - курсив
        <u> </u> - подчеркивание
    """


@bot.message_handler(commands=['Dinozavrik_Secret_Diary'])
async def info_command(message):
    # Отправляем пользователю информацию о боте
    await bot.send_message(message.chat.id, "Ooow, it's so cute that you want to know about me."
                                            "\nI was born 13.11.2024.\nOn first day of my life could answer only for /start."
                                            "\n(14.11.2024) I can answer for привет."
                                            "\n\nShe needed some rest and time to do somethings for university."
                                            "\nI miss you, mum...\n"
                                            "\nToday (05.12.2024)I have button to supply you action with file.")

"""
@bot.message_handler(content_types=['photo'])
async def get_picture(message):
    await bot.reply_to(message, "I know him! So handsome!")
"""
#######################################################################################################
# Функция временного хранения файла: сохранение -> (обработка) -> удаление


def delete_files_in_directory(directory_path):
    # Проверяем, существует ли папка
    if not os.path.exists(directory_path):
        return f"Папка '{directory_path}' не существует."

    """
    # Подтверждение пользователя
    confirmation = input(f"Вы уверены, что хотите удалить все файлы из '{directory_path}'? (да/нет): ")
    if confirmation.lower() != 'да':
        return "Удаление отменено."
    """

    results = []  # Список для накопления результатов
    # Проходим по всем файлам и папкам в директории
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # Удаляем файл
                results.append(f"Файл '{file_path}' удалён.")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Удаляем директорию и её содержимое
                results.append(f"Папка '{file_path}' и все её содержимое удалены.")
        except Exception as e:
            results.append(f"Ошибка при удалении '{file_path}': {e}")

    return "\n".join(results)  # Возвращаем все результаты как строку


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
            text = 'Преобразованный файл: '
            await bot.answer_callback_query(call.id)  # Подтверждение нажатия на кнопку
            await bot.send_message(call.message.chat.id, text)
            #await bot.send_message()

        elif call.data == 'compare':
            text = 'Сравнение: '
            await bot.answer_callback_query(call.id)
            await bot.send_message(call.message.chat.id, text)
            answer = compare_files(file1, file2)
            delete_files_in_directory(SAVE_FOLDER) # Очистка папки SAVE_FOLDER
            answer = answer +'\nПапка SAVE_FOLDER очищена! 🗑️'
            await bot.send_message(call.message.chat.id, answer)

        elif call.data == 'rename':
            text = 'Так гораздо лучше!\nПереименованный файл: '
            await bot.answer_callback_query(call.id)
            await bot.send_message(call.message.chat.id, text)
    else:
        await bot.send_message(call.message.chat.id, 'Недостаточно файлов в папке.')




SAVE_FOLDER = 'Pro/Fun/saveFiles'

# Убедитесь, что папка существует
if not os.path.exists(SAVE_FOLDER):
    #os.makedirs(SAVE_FOLDER)
    os.mkdir(SAVE_FOLDER)

# Список для хранения файлов
user_files = []

@bot.message_handler(content_types=['document'])  # Обработка документов
async def handle_file(message):
    user_files.append(message.document.file_id)  # Сохраняем file_id в список
    # Отладочное сообщение для проверки file_id
    await bot.send_message(message.chat.id,
                           f"Файл принят! Ваш file_id: {message.document.file_id}. Вы можете отправить команду /save_file_for_work для сохранения.")

@bot.message_handler(commands=['save_file_for_work'])  # Обработчик для команды /save_file_for_work
async def save_files_command(message):
    if not user_files:
        await bot.send_message(message.chat.id, "Нет файлов для сохранения! 📂")
        return

    for file_id in user_files:
        # Отладочное сообщение для проверки file_id
        await bot.send_message(message.chat.id, f"Пытаюсь загрузить файл с file_id: {file_id}")

        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        # Загружаем файл
        try:
            downloaded_file = await bot.download_file(file_path)
            file_name = file_info.file_path.split('/')[-1]  # Получаем имя файла из пути
            file_save_path = os.path.join(SAVE_FOLDER, file_name)

            # Сохраняем файл
            with open(file_save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            await bot.send_message(message.chat.id,
                                   f"Файл {file_name} успешно сохранен в {file_save_path}.")  # Отладочное сообщение
        except Exception as e:
            await bot.send_message(message.chat.id, f" [!] Ошибка при сохранении файла {file_name}: {e}")
            return

        user_files.clear()  # Очищаем список после сохранения

        # Проверяем наличие файлов в папке
        if os.listdir(SAVE_FOLDER):  # Если папка не пустая
            await bot.send_message(message.chat.id, "Файлы успешно сохранены! 🎉")
        else:
            await bot.send_message(message.chat.id,
                                   "Не удалось сохранить файлы. 😟 Проверьте, есть ли файлы для сохранения.")
#########################################################################################################################################

# Эта функция обрабатывает текстовые сообщения от пользователя
@bot.message_handler(func=lambda message: True)  # функция будет принимать все текстовые сообщения
async def hola(message):
    # Приводим текст сообщения к нижнему регистру для удобства сравнения
    text = message.text.lower()

    # Проверяем, написал ли пользователь "привет"
    if text == "привет":
        # Отправляем приветственное сообщение
        await bot.send_message(message.chat.id,
                               f"Hola, {message.from_user.first_name}!\nI am dinozavrik Metadoc.\nRight now my mum and I are learning how to work with files and messages from you.\nI hope this will help me make your life easier.\nLet's be friends.🌸")

    # Проверяем, написал ли пользователь "id"
    elif text == 'id':
        # Отправляем ID пользователя
        await bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        await bot.send_message(message.chat.id, "😭")
        await bot.reply_to(message, "Мне это не понятно \n Давай ты ещё разок напишешь")
        await bot.send_message(message.chat.id, "🥹")
