from bot import dp, bot, UserStates
import database
import ui
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


# Админ панель
@dp.message_handler(commands='admin')
async def show_admin_panel(message: types.Message):
    if database.get_user_rights(message.from_user.id) <= 0:
        await message.answer(ui.TEXT_RIGHTS_MISSED)
        return

    if database.get_user_block(message.from_user.id):
        await message.answer(ui.TEXT_YOU_ARE_BLOCKED)
        return

    await UserStates.admin.set()

    await message.answer(ui.TEXT_ADMIN_MENU_OPENED, reply_markup=ui.keyboard_admin)


# Добавить задание
@dp.message_handler(Text(equals=ui.BUT_TASK_ADD), state=UserStates.admin)
async def show_add_task(message: types.Message):
    await UserStates.task_add_enter.set()

    await message.answer(ui.TEXT_TASK_ADD, reply_markup=None)


# Перехватчик ввода названия нового задания
@dp.message_handler(state=UserStates.task_add_enter)
async def enter_new_task(message: types.Message):
    await UserStates.admin.set()

    database.add_task(message.from_user.id, message.text)

    await message.answer(ui.TEXT_TASK_ADDED, reply_markup=ui.keyboard_admin)


# Показ изменяемых заданий
@dp.message_handler(Text(equals=ui.BUT_TASK_EDIT), state=UserStates.admin)
async def show_edit_tasks(message: types.Message):
    tasks = database.get_tasks()

    inline_tasks = types.InlineKeyboardMarkup()
    for task in tasks:
        inline_tasks.insert(types.InlineKeyboardButton(ui.TEXT_TASKS_LINE.format(name=task['name'], points=task['points']), callback_data=f"taskedit_{task['id']}"))

    await message.answer(ui.TEXT_TASKS, reply_markup=inline_tasks)


# Показ изменяемых пользователей
@dp.message_handler(Text(equals=ui.BUT_USER_EDIT), state=UserStates.admin)
async def show_edit_users(message: types.Message):
    users = database.get_users()

    inline_users = types.InlineKeyboardMarkup()
    for user in users:
        inline_users.insert(types.InlineKeyboardButton(ui.TEXT_USERS_LINE.format(id=user['id'], name=user['name']), callback_data=f"useredit_{user['id']}"))

    await message.answer(ui.TEXT_USERS, reply_markup=inline_users)