from aiogram import Bot, Dispatcher, executor, types
import random
import string

from config import TOKEN_API

HELP_COMMAND = '''
/help - список команд
/start - начать работу с ботом
/description - описание бота
/count - выводит число собственных предыдущих вызовов
'''

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

count = 0

# порядок хэндлеров очень важен
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать')
    await message.delete()

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)

@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.reply(text='это просто бот, который ничего не делает')

@dp.message_handler(commands=['count'])
async def count_command(message: types.Message):
    global count
    await message.answer(f'COUNT: {count}')
    count += 1

@dp.message_handler()
async def check_zero(message: types.Message):
    if '0' in message.text:
        return await message.reply(text='YES')
    await message.reply(text='NO')

@dp.message_handler()
async def send_random_letter(message: types.Message):
    await message.answer(random.choice(string.ascii_letters))

if __name__ == '__main__':
    executor.start_polling(dp)
