import datetime
from bot import dp
import database
import ui
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


# Хэндлер запуска
@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await dp.bot.set_my_commands(ui.commands)  # Установка комманд

    user = database.get_user(message.from_user.id)
    
    time_dif = database.get_start_time() - datetime.datetime.now()
    seconds_dif = time_dif.days * 24 * 60 * 60 + time_dif.seconds

    text = ''
    if not user:  # Проверка на регистрацию в боте
        database.add_user(message.from_user.id, str(message.from_user.full_name))
        text = ui.TEXT_USER_START_NEW
    else:
        text = ui.TEXT_USER_START

    await message.answer(text.format(
        username=message.from_user.full_name, 
        hours=seconds_dif // 3600,
        minutes=seconds_dif % 3600 // 60,
        seconds=seconds_dif % 60), 
        reply_markup=ui.keyboard_main)


# Хэндлер меню помощи
@dp.message_handler(commands='help', state='*')
@dp.message_handler(Text(equals=ui.BUT_HELP))
async def cmd_help(message: types.Message):
    await message.answer(ui.TEXT_HELP, parse_mode='html')


# Возвращение назад
@dp.message_handler(commands='back', state='*')
@dp.message_handler(Text(equals=ui.BUT_BACK), state='*')
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(ui.TEXT_BACK, reply_markup=ui.keyboard_main)
