import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import database
import ui
from bot import dp


# Хэндлер запуска
@dp.message_handler(commands='start', state='*')
async def show_start(message: types.Message, state: FSMContext):
    await state.finish()
    await dp.bot.set_my_commands(ui.commands)  # Установка комманд

    user = database.get_user(message.from_user.id)

    text = ''
    if not user:  # Проверка на регистрацию в боте
        database.add_user(message.from_user.id, str(
            message.from_user.full_name))
        text = ui.TEXT_USER_START_NEW
    else:
        text = ui.TEXT_USER_START

    await message.answer(text.format(
        username=message.from_user.full_name),
        reply_markup=ui.keyboard_main)


# Хэндлер меню помощи
@dp.message_handler(commands='help', state='*')
@dp.message_handler(Text(equals=ui.BUT_HELP))
async def show_help(message: types.Message):
    await message.answer(ui.TEXT_HELP, parse_mode='html')


def get_time_dif(time_dif: datetime.timedelta):
    seconds_dif = time_dif.days * 24 * 60 * 60 + time_dif.seconds

    hours = seconds_dif // 3600
    minutes = seconds_dif % 3600 // 60
    seconds = seconds_dif % 60
    return (hours, minutes, seconds)


# Хэндлер главного меню
@dp.message_handler(commands='main', state='*')
@dp.message_handler(Text(equals=ui.BUT_MAIN))
async def show_main(message: types.Message):
    start_time = database.get_start_time()
    end_time = database.get_end_time()

    is_started = start_time < datetime.datetime.now()
    is_ended = end_time < datetime.datetime.now()

    hours, minutes, seconds = get_time_dif(
        start_time - datetime.datetime.now())

    text = ui.TEXT_MAIN
    if start_time and not is_started:
        text += (ui.TEXT_MAIN_START_TIME + ui.TEXT_MAIN_START_TIME_REMAIN).format(
            start_time=start_time.strftime("%d.%m.%Y %H:%M:%S"), time_remaining=f'{hours}:{minutes}:{seconds}')

    hours, minutes, seconds = get_time_dif(end_time - datetime.datetime.now())

    if end_time and not is_ended:
        text += (ui.TEXT_MAIN_END_TIME + ui.TEXT_MAIN_END_TIME_REMAIN).format(
            end_time=end_time.strftime("%d.%m.%Y %H:%M:%S"), time_remaining=f'{hours}:{minutes}:{seconds}')

    if start_time and not is_started:
        text += ui.TEXT_MAIN_NOT_STARTED

    if (is_started and not is_ended) or (not start_time and not is_ended) or (not start_time and not end_time):
        text += ui.TEXT_MAIN_STARTED

    if end_time and is_ended:
        text += ui.TEXT_MAIN_ENDED

    await message.answer(text, reply_markup=ui.keyboard_main)


# Возвращение назад
@dp.message_handler(commands='back', state='*')
@dp.message_handler(Text(equals=ui.BUT_BACK), state='*')
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(ui.TEXT_BACK, reply_markup=ui.keyboard_main)
