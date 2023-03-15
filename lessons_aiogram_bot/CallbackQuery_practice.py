from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

ikb = InlineKeyboardMarkup()
ib1 = InlineKeyboardButton(text='нра', callback_data='like')
ib2 = InlineKeyboardButton(text='не нра', callback_data='dislike')
ib3 = InlineKeyboardButton(text='закрыть', callback_data='close')

ikb.add(ib1, ib2).add(ib3)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://i.pinimg.com/originals/74/19/7b/74197bfe982c148b61d65d56f0ad8501.jpg',
                         caption='Нра?',
                         reply_markup=ikb)

@dp.callback_query_handler(text='close')
async def ikb_close_cb_handler(callback: types.CallbackQuery):
    await callback.message.delete()

@dp.callback_query_handler()
async def ikb_cb_handler(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer('Тебе понравилось')
    elif callback.data == 'dislike':
        await callback.answer('Тебе не понравилось')
    await callback.answer('Закрыть')

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
