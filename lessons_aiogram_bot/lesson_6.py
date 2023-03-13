# Для отправки контента пользователю используется функция send_something, в аргумент chat_id которой указывают ID чата, куда боту необходимо отправлять 
# сообщение.
# Если мы хотим отправить сообщение в личку, то мы будем использовать message.from_user.id, если хотим отправить в группу, то мы используем message.chat.id

# метод message.answer - всегда отправляет сообщение в то место, куда пользователь отправил сообщение
# у данного метода есть аргумент text = сообщение; аргумент parse_mode = тип разметки

# метод bot.send_photo() - отправляет фотографию. Аргументы метода chat_id = id чата; аргумент photo = ссылка на фото

# метод bot.send_location() - отправляет местоположение. Аргемент chat_id = id чата; latitude, longitude = широта и долгота

from aiogram import Bot, Dispatcher, types, executor

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP_COMMAND = '''
<b>/start</b> - <em>начало работы</em>
<b>/help</b> - <em>начало работы</em>
<b>/картинка</b> - <em>начало работы</em>
'''

@dp.message_handler(commands=['location'])
async def send_location(message: types.Message):
    await bot.send_location(chat_id = message.from_user.id,
                            latitude=55,
                            longitude=74)

# комманда help отправляется в личку, несмотря на то, что отправляем команду в группу
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id = message.from_user.id, 
                           text=HELP_COMMAND,
                           parse_mode='HTML')
    await message.delete()

@dp.message_handler(commands=['картинка'])
async def send_image(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo='https://assets.mycast.io/posters/lemony-snicket-s-a-series-of-unfortunate-events-part-ii-2006-fan-casting-poster-150008-large.jpg?1638310138')
    await message.delete()


@dp.message_handler()
async def echo(message: types.Message):
    ##await message.answer(message.text)
    #await  bot.send_message(chat_id=message.chat.id,
    #                        text='Hello')
    # вывод - эти два метода абсолютно тождественны
    # но если записать так, то бот будет отправлять сообщения в личку, даже если пользователь написал в группу
    await bot.send_message(chat_id = message.from_user.id,
                           text='hello')


# skip_updates используется для того, чтобы все обновления в боте пропускались. Т.е. если бот не онлайн, но ему приходят сообщения, то он не будет на них
# реагировать при запуску
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





