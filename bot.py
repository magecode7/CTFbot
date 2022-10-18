import logging
import config
import random
import database
import datetime
import ui
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Логирование
# logging.basicConfig(filename='bot.log', level=logging.DEBUG)
# Хранилище состояний
storage = MemoryStorage()


# Состояния
class UserStates(StatesGroup):
    admin = State()
    user_change_name = State()
    task_add_enter = State()
    task_edit = State()
    task_edit_enter = State()
    task_edit_name = State()
    task_edit_desc = State()
    task_edit_flag = State()
    task_edit_points = State()
    task_file_add = State()
    task_flag_enter = State()
    user_edit = State()
    user_edit_name = State()
    user_edit_rights = State()


# Бот токен
bot = Bot(token=config.TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot, storage=storage)
# База данных бота
database.create_tables()
if not database.get_user(config.ADMIN):
    database.add_user(config.ADMIN, 'admin', 5)


# Хэндлер запуска
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await dp.bot.set_my_commands(ui.commands)  # Установка комманд

    user = database.get_user(message.from_user.id)
    
    if not user:  # Проверка на регистрацию в боте
        database.add_user(message.from_user.id, message.from_user.full_name)
        await message.answer(ui.TEXT_USER_START_NEW.format(username=message.from_user.full_name, time=datetime.datetime.now().strftime("%m.%d.%Y, %H:%M:%S")), reply_markup=ui.keyboard_main)
    else:
        await message.answer(ui.TEXT_USER_START.format(username=message.from_user.full_name, time=datetime.datetime.now().strftime("%m.%d.%Y, %H:%M:%S")), reply_markup=ui.keyboard_main)


# Хэндлер меню помощи
@dp.message_handler(commands='help')
async def cmd_help(message: types.Message):
    await message.answer(ui.TEXT_HELP, parse_mode='html')


# Возвращение назад
@dp.message_handler(commands='back', state=UserStates.all_states)
@dp.message_handler(Text(equals=ui.BUT_BACK), state=UserStates.all_states)
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(ui.TEXT_BACK, reply_markup=ui.keyboard_main)


def start_bot():  # Запуск бота
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    start_bot()
