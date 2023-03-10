from aiogram import Bot, Dispatcher, types, executor

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

# если мы не отправляем обычное сообщение, то необходимо указать чему равен контент
@dp.message_handler(content_types=['sticker'])
# принимает на вход тип Message, потому что это также сообщение
async def send_sticker_id(message: types.Message):
    await message.answer(message.sticker.file_id)

if __name__ == '__main__':
    executor.start_polling(dp)
