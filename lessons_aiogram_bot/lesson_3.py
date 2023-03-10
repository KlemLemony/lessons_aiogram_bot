from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

# это сообщение выведется в консоль
async def on_startup(_):
    print('бот был успешно запущен')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
# parse_mode - параметр, который принимает тот тип чтения сообщений, который необходим
    await message.answer('<em>Привет, добро пожаловать</em>', parse_mode='HTML')

# стикеры
@dp.message_handler(commands=['give'])
async def send_sticker(message: types.Message):
    # в аргументах указываем ID чата - куда нужно отправить сообщение
    # в методе answer он не нужен, а вот здесь нужен
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEIE3lkCyjTHamL0UTyow0R73XfL8LNbQACzBAAAr8M0ErYqDe37o7zay8E')
    # можем удалить сообщение /give, чтобы не было много спама
    await message.delete()

# хэндлер эхо-бот, но прибавляет к сообщению эмодзи
@dp.message_handler()
async def send_emoji(message: types.Message):
    await message.reply(message.text + '🧚🏻‍♂️')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
