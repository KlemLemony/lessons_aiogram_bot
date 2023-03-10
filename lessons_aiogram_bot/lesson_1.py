from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN_API

bot = Bot(TOKEN_API) # создаем экземпляр класса bot
dp = Dispatcher(bot) # осуществляет анализ всех входящих апдейтов, отвечает за функционал бота

# хэндлер используется для того, чтобы отлавливать, анализировать и обрабатывать входящие сообщения
@dp.message_handler()
# в качестве аргумента, функция получает входящее сообщение, которое отправляет пользователь
# должна быть своеобразная аннотация типов. В качестве аннотации типов будем обращаться к модулю types
# ассинхронная функция срабатывает, потому что есть хэндлер
async def echo(message: types.Message):
    if len(message.text.split()) == 2:
        await message.answer(text=message.text.upper()) # написать сообщение. В скобках указываем аргумент text

# если данный модуль будет запускаться самостоятельно...
if __name__ == '__main__':
    executor.start_polling(dp)