import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.dispatcher.filters import Command

storage: MemoryStorage = MemoryStorage()
scheduler = AsyncIOScheduler()

TOKEN_API = '5992630905:AAG7ElCyihaRKDoBwxvx5_uEPbch5dR5ZGg'
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot,
                storage=storage)

scheduler.start()

class Form(StatesGroup):
    is_everything_ok = State()
    remember_oath = State()

@dp.message_handler(commands=["pupuce"])
async def start_cmd_handler(message: types.Message):
    await Form.is_everything_ok.set()

    await bot.send_message(chat_id = message.from_user.id, text='У тебя все хорошо?')

@dp.message_handler(state=Form.is_everything_ok)
async def process_is_everything_ok(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.reply("ну и чудненько")
        await Form.remember_oath.set()
        await message.reply("А ты помнишь клятву на пальчиках?")
    elif message.text.lower() == 'нет':
        await message.reply("если честно, мне все равно. Я просто спросил")
        await Form.remember_oath.set()
        await message.reply("А ты помнишь клятву на пальчиках?")
    else:
        await message.reply("чего блять? Ты пожешь написать да или нет?")

@dp.message_handler(state=Form.remember_oath)
async def process_remember_oath(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.reply("япикаееееей, мазафака. Тогда до встречи! Счастья, здоровья тебе")
    elif message.text.lower() == 'нет':
        await message.reply("Но ведь мы клялись на пальчиках! Пидор!")
    else:
        await message.reply("чего блять? Ты пожешь написать да или нет?")

    await state.finish()

async def scheduled(scheduler):
    scheduler.add_job(start_cmd_handler, 'interval', seconds=15, id='start_cmd_handler')

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)


