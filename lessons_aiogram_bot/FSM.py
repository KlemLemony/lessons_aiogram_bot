from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage # MemoryStorage - класс, который отвечает за создание экземпляра локального хранилища, в котором мы содержим данные о состояниях
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

storage = MemoryStorage() # это экземпляр хранилище, в котором хранятся состояния
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

# создаем класс, который будет хранить в себе все необходимые состояний бота
class ProfileStatesGroup(StatesGroup): # класс psg наследуется от sg
   photo = State() # состояние ожидания фото
   name = State() # состояние ожидания имени
   age = State() # состояние ожидания возраста
   description = State() # состояние ожидания описания

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))
    return kb

# обработчик команды cancel
@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply('вы прервали создание анкеты',
                        reply_markup=get_kb())

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) ->None:
    await message.answer('чтобы создать профиль введите комманду create',
                         reply_markup=get_kb())

@dp.message_handler(commands=['create'])
async def cmd_start(message: types.Message) ->None:
    await message.reply('давайте создадим профиль. Для начала отправь фото',
                        reply_markup=get_cancel_kb())
    # обращаемся к классу, который хранит состояния. В нем обращаемся к нужному нам атрибуту (в данном случае photo) или по другому - состоянию. И установим это состояние с помощью метода set                               
    await ProfileStatesGroup.photo.set()
    # теперь состояние бота установлено на photo. Он будет находится в ожидании фотографии

# размещаем доп проверку для того, чтобы быть уверенным, что пользователь отправил именно фото
# если отправлена не фото, то срабатывает этот хэндлер
@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.photo) # устанавливаем фильтр, который проверяет действительно ли отправленна фотка
async def check_photo(message: types.Message):
    await message.reply('это не фото')

@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.photo) # здесь прописываем состояние state для того, чтобы этот хэндлер обробатывал входящие фото только если у него в состоянии state выставленно photo
async def load_photo(message: types.Message, state: FSMContext): # здесь обязательно пишем второй аргумен state
    # далее используем менеджер контекста with для того, чтобы открыть локальное хранилище данных, где будем хранить временно данные, отправленной фото
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    
    await message.reply('теперь отправь свое имя')
    # меняем состояние бота на следующее состояние. Т.е. следующее состояние бота - name
    await ProfileStatesGroup.next()

# проверка на корректность возраста
@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100, state=ProfileStatesGroup.age)
async def check_age(message: types.Message):
    await message.reply('введите реальный возраст')

@dp.message_handler(state=ProfileStatesGroup.name) 
async def send_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Сколько тебе лет')
    await ProfileStatesGroup.next()

@dp.message_handler(state=ProfileStatesGroup.age) 
async def send_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply('Расскажи о себе')
    await ProfileStatesGroup.next()

@dp.message_handler(state=ProfileStatesGroup.description)
async def send_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        #print(data) # выводим данные, которые сохранили, в консоль, чтобы удостовериться, что все работает
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=f"{data['name']}, {data['age']}, {data['description']}")

    await message.reply('Ваша анкета успешно создана')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)






