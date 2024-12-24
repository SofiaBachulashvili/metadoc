from telebot import types
import os
import shutil

from .botik import bot  # Импортируем объект бота, используя относительный путь .botik
from .compareFILES.compareFun import compare_files

# Обработчик для команд /start, /Hello, /Hola
@bot.message_handler(commands=['start', 'Hello', 'Hola'])
async def start_command(message):
    await bot.send_message(message.chat.id,
                           f"Hola, {message.from_user.first_name}!\nI am dinozavrik Metadoc🦕\nLet's be friends.🌸\nI am learning to work with files.")


@bot.message_handler(commands=['help'])  # Обрабатываем команду /help
async def help_command(message):
    # Определяем список доступных команд
    commands_list = [
        '/start - Начало общения с ботом',
        '/help - Получить список доступных команд',
        '/handle_document - Переименовать документ',
        '/save_file_for_work - Сохранить файл для обработки',
        '/click - Выбор действия с файлом',
        #'/Dinozavrik_Secret_Diary - Узнать историю Dinozavrika'
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

#######################################################################################################
# Функция временного хранения файла: сохранение -> (обработка) -> удаление


def delete_directory(directory_path):
    # Функция для удаления директории и всех её содержимых файлов и папок.
    # :param directory_path: Путь к папке, которую нужно удалить
    # :return: Результат удаления

    # Проверяем, существует ли папка
    if not os.path.exists(directory_path):
        return f"Папка '{directory_path}' не существует."

    # # Подтверждение пользователя
    # confirmation = input(f"Вы уверены, что хотитееееееееееееееее удалить '{directory_path}' вместе со всем содержимым? (да/нет): ")
    # if confirmation.lower() != 'да':
    #     return "Удаление отменено."

    try:
        shutil.rmtree(directory_path)  # Удаляем директорию и её содержимое
        return f"Папка '{directory_path}' и все её содержимое были удалены."
    except Exception as e:
        return f"[!] Ошибка при удалении '{directory_path}': {e}"


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
    user_id = call.from_user.id # Получаем ID пользователя
    user_folder = os.path.join('Pro/Fun/saveFiles', str(user_id))  # Папка пользователя
    # Получаем список всех файлов в папке
    files = [f for f in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, f))]
    # Сортируем файлы по времени модификации и берем последние два
    files.sort(key=lambda x: os.path.getmtime(os.path.join(user_folder, x)), reverse=True)

    # Получаем адреса последних двух файлов
    if len(files) >= 2:
        file1 = os.path.join(user_folder, files[0])
        file2 = os.path.join(user_folder, files[1])

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
            #delete_directory(user_folder) # Удаление папки user_folder
            answer = answer +'\n\nПапка user_folder удалена! 🗑️'
            await bot.send_message(call.message.chat.id, answer)

        elif call.data == 'rename':
            text = 'Так гораздо лучше!\nПереименованный файл: ✅✅✅✅✅'
            await bot.answer_callback_query(call.id)
            await bot.send_message(call.message.chat.id, text)
    else:
        await bot.send_message(call.message.chat.id, 'Недостаточно файлов в папке.')


# Список для хранения файлов
user_files = []

@bot.message_handler(content_types=['document'])  # Обработка документов
async def handle_file(message):
    user_files.append(message.document.file_id)  # Сохраняем file_id в список
    user_id = message.from_user.id  # Получаем ID пользователя

    # Убедитесь, что папка для данного пользователя существует
    user_folder = os.path.join('Pro/Fun/saveFiles', str(user_id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Отладочное сообщение для проверки file_id и user_id
    await bot.send_message(message.chat.id,
                           f"Файл принят!\nВаш file_id: {message.document.file_id}.\n"
                           f"ID вашего аккаунта: {user_id}.\n"
                           "Вы можете отправить команду /save_file_for_work для сохранения.")

@bot.message_handler(commands=['save_file_for_work'])  # Обработчик для команды /save_file_for_work
async def save_files_command(message):
    user_id = message.from_user.id  # Получаем ID пользователя
    user_folder = os.path.join('Pro/Fun/saveFiles', str(user_id))  # Папка пользователя

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
            file_save_path = os.path.join(user_folder, file_name)

            # Сохраняем файл
            with open(file_save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            await bot.send_message(message.chat.id,
                                   f"Файл {file_name} успешно сохранен в {file_save_path}.")  # Отладочное сообщение
        except Exception as e:
            await bot.send_message(message.chat.id, f"Ошибка при сохранении файла {file_name}: {e}")
            return

        user_files.clear()  # Очищаем список после сохранения

        # Проверяем наличие файлов в папке
        if os.listdir(user_folder):  # Если папка не пустая
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
        await bot.reply_to(message, "Мне это не понятно \nДавай ты ещё разок напишешь")
        await bot.send_message(message.chat.id, "🥹")
