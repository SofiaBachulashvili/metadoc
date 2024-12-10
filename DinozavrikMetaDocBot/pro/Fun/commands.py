from .botik import bot  # Импортируем экземпляр бота, используя относительный путь .botik
# Использование точки перед botik означает, что модуль будет искаться в текущей директории

from telebot import types
import os

from .botik import bot  # Импортируем объект бота
from telebot import types
from .compareFILES.compareFun import compare_files
import os

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


@bot.message_handler(content_types=['document'])  # Обработка документов
async def handle_file(message):
    user_files.append(message.document.file_id)  # Сохраняем file_id

    await bot.send_message(message.chat.id,
                           "Файл принят! Вы можете отправить команду /save_file_for_work для сохранения.")


SAVE_FOLDER = 'Pro/Fun/compareFILES/saveFiles'

# Убедитесь, что папка существует
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Список для хранения файлов
user_files = []
@bot.message_handler(commands=['save_file_for_work'])  # Обработчик для команды /save_file_for_work
async def save_files_command(message):
    if not user_files:
        await bot.send_message(message.chat.id, "Нет файлов для сохранения! 📂")
        return

    for file_id in user_files:
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
            print(f"Файл {file_name} успешно сохранен в {file_save_path}")  # Отладочное сообщение
        except Exception as e:
            print(f"Ошибка при сохранении файла {file_name}: {e}")

    user_files.clear()  # Очищаем список после сохранения

    # Проверяем наличие файлов в папке
    if os.listdir(SAVE_FOLDER):  # Если папка не пустая
        await bot.send_message(message.chat.id, "Файлы успешно сохранены! 🎉")
    else:
        await bot.send_message(message.chat.id, "Не удалось сохранить файлы. 😟 Проверьте, есть ли файлы для сохранения.")







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



# Возможно, вы хотите добавить дополнительно функцию для удаления файлов
@bot.message_handler(commands=['delete_file'])  # Обрабатываем команду /delete_file
async def delete_file(message):
    files = os.listdir('saveF')
    if not files:
        await bot.send_message(message.chat.id, "Папка 'saveF' уже пуста! 🗑️")
        return

    # Удаляем первый файл из папки для примера
    file_to_delete = os.path.join('saveF', files[0])
    os.remove(file_to_delete)

    await bot.send_message(message.chat.id, f"Файл '{files[0]}' удалён из папки 'saveF'. ✨")


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
