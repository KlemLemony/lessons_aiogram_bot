#CallbackQuery - класс, каждый экземпляр которого представляет конкретный callback запрос,
# генерируемый Telegram API при каком-либо событии, например при нажатии на кнопку в инлайн клавиатуре

# Каждый его экземпляр обычно обозначается, как call или callback в пределах обработки хэндлером.
# (Это как когда мы писали message: types.Message)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN_API

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('❤️', callback_data='like'), InlineKeyboardButton('🖕🏻', callback_data='dislike')]
    ])

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://i.pinimg.com/originals/74/19/7b/74197bfe982c148b61d65d56f0ad8501.jpg',
                         caption='Нравится?',
                         reply_markup=ikb)

@dp.callback_query_handler()
async def ikb_cb_handler(callback: types.CallbackQuery):
    print(callback)
    if callback.data == 'like':
        await callback.answer('Тебе понравилось')
    await callback.answer('Тебе не понравилось')

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
