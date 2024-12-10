import asyncio
from Fun.buttons import *  # Импортируем все обработчики из второго файла команд
from Fun.commands import *  # Импортируем все обработчики из первого файла команд
#import Fun.commands

from Fun.botik import bot  # Импортируем экземпляр бота

if __name__ == "__main__":
    print("Starting the bot...")
    #Fun.commands.
    asyncio.run(bot.polling(non_stop=True))  # Запускаем бота
