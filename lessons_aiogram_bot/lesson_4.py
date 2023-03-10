from aiogram import Bot, Dispatcher, types, executor

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP_COMMAND = '''
<b>/help</b> - <em>показываем список команд</em>
<b>/give</b> - <em>отправляет котика</em>
<b>/start</b> - <em>запускает бота</em>
'''

async def on_startup(_):
    print('я запустился')

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND, parse_mode='HTML')

@dp.message_handler()
async def count_check_mark(message: types.Message):
    await message.answer(text=str(message.text.count('✅')))

@dp.message_handler(commands=['give'])
async def send_sticker(message: types.Message):
    await message.answer(text='Смотри какой смешной кот' + '❤️')
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEIE3lkCyjTHamL0UTyow0R73XfL8LNbQACzBAAAr8M0ErYqDe37o7zay8E')

# если нужна обработка обычного текстового сообщения, то в хэндлер ничего не пишем
@dp.message_handler()
async def send_hurt(message: types.Message):
    if message.text == '❤️':
        await message.answer('🌞')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
