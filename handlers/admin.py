import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from filters.rights import MinRightsFilter

import database
import ui
from bot import BotStates, bot, dp


# Админ панель
@dp.message_handler(MinRightsFilter(1), commands='admin')
async def show_admin_panel(message: types.Message):
    if database.get_user_block(message.from_user.id):
        await message.answer(ui.TEXT_YOU_ARE_BLOCKED)
        return

    await BotStates.admin.set()

    await message.answer(ui.TEXT_ADMIN_MENU_OPENED, reply_markup=ui.keyboard_admin)


# Добавить задание
@dp.message_handler(Text(equals=ui.BUT_TASK_ADD), MinRightsFilter(1), state=BotStates.admin)
async def show_add_task(message: types.Message):
    await BotStates.task_add_enter.set()

    await message.answer(ui.TEXT_TASK_ADD, reply_markup=ui.keyboard_back)


# Перехватчик ввода названия нового задания
@dp.message_handler(state=BotStates.task_add_enter)
async def enter_new_task(message: types.Message):
    if len(message.text) > 16:
        await message.answer(ui.TEXT_TASK_ADD_OUTBOUND)
        return

    database.add_task(message.from_user.id, message.text)

    await BotStates.admin.set()

    await message.answer(ui.TEXT_TASK_ADDED, reply_markup=ui.keyboard_admin)


# Показ изменяемых заданий
@dp.message_handler(Text(equals=ui.BUT_TASK_EDIT), state=BotStates.admin)
async def show_edit_tasks(message: types.Message):
    tasks = database.get_tasks()

    inline_tasks = types.InlineKeyboardMarkup()
    for task in tasks:
        inline_tasks.insert(types.InlineKeyboardButton(ui.TEXT_TASKS_LINE.format(
            name=task['name'], points=task['points']), callback_data=f"taskedit_{task['id']}"))

    await message.answer(ui.TEXT_TASKS, reply_markup=inline_tasks)


# Показ изменяемых пользователей
@dp.message_handler(Text(equals=ui.BUT_USER_EDIT), state=BotStates.admin)
async def show_edit_users(message: types.Message):
    users = database.get_users()

    inline_users = types.InlineKeyboardMarkup()
    for user in users:
        inline_users.insert(types.InlineKeyboardButton(ui.TEXT_USERS_LINE.format(
            id=user['id'], name=user['name']), callback_data=f"useredit_{user['id']}"))

    await message.answer(ui.TEXT_USERS, reply_markup=inline_users)


# Рассылка сообщений
@dp.message_handler(Text(equals=ui.BUT_BROADCAST), MinRightsFilter(4), state=BotStates.admin)
async def show_broadcast(message: types.Message):
    await BotStates.broadcast_enter.set()

    await message.answer(ui.TEXT_BROADCAST_ENTER, reply_markup=ui.keyboard_back)


# Перехватчик ввода сообщения рассылки
@dp.message_handler(state=BotStates.broadcast_enter)
async def broadcast_enter(message: types.Message):
    if len(message.text) > 512:
        await message.answer(ui.TEXT_BROADCAST_ENTER_OUTBOUND)
        return

    users = database.get_users()

    for user in users:
        if user['id'] != message.from_user.id:
            await bot.send_message(user['id'], message.text)

    await BotStates.admin.set()

    await message.answer(ui.TEXT_BROADCAST_SEND, reply_markup=ui.keyboard_admin)


# Запрос в БД
@dp.message_handler(Text(equals=ui.BUT_DATABASE_QUERY), MinRightsFilter(5), state=BotStates.admin)
async def show_database_query(message: types.Message):
    await BotStates.database_query_enter.set()

    await message.answer(ui.TEXT_QUERY_ENTER, reply_markup=ui.keyboard_back)


# Перехватчик ввода запроса в БД
@dp.message_handler(state=BotStates.database_query_enter)
async def database_query_enter(message: types.Message):
    database.send_query(message.text)

    await BotStates.admin.set()

    await message.answer(ui.TEXT_QUERY_SEND, reply_markup=ui.keyboard_admin)


# Сброс соревнований
@dp.message_handler(Text(equals=ui.BUT_RESET), MinRightsFilter(5), state=BotStates.admin)
async def show_reset(message: types.Message):
    database.reset_competitions()

    await message.answer(ui.TEXT_RESETED)


# Показ установки времени начала
@dp.message_handler(Text(equals=ui.BUT_TIME_START_SET), MinRightsFilter(4), state=BotStates.admin)
async def show_time_start(message: types.Message):
    await BotStates.time_start_set.set()

    await message.answer(ui.TEXT_TIME_START_SET)


# Хендлер установки времени начала
@dp.message_handler(state=BotStates.time_start_set)
async def time_start_set(message: types.Message):
    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y %H:%M:%S")

        database.set_start_time(date)

        await BotStates.admin.set()

        await message.answer(ui.TEXT_TIME_START_SETTED)
    except Exception as e:
        await message.answer(ui.TEXT_TIME_SET_ERROR)


# Показ установки времени окончания
@dp.message_handler(Text(equals=ui.BUT_TIME_END_SET), MinRightsFilter(4), state=BotStates.admin)
async def show_time_end(message: types.Message):
    await BotStates.time_end_set.set()

    await message.answer(ui.TEXT_TIME_END_SET)


# Хендлер установки времени окончания
@dp.message_handler(state=BotStates.time_end_set)
async def time_end_set(message: types.Message):
    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y %H:%M:%S")

        database.set_end_time(date)

        await BotStates.admin.set()

        await message.answer(ui.TEXT_TIME_END_SETTED)
    except Exception as e:
        await message.answer(ui.TEXT_TIME_SET_ERROR)
