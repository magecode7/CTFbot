import logging
import configparser
import random
import database
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
    enter_add = State()
    edit = State()
    edit_enter = State()
    edit_name = State()
    edit_desc = State()
    edit_flag = State()
    edit_points = State()
    enter_flag = State()


# Конфиг
config = configparser.ConfigParser()
config.read('config.ini')
# Бот токен
bot = Bot(token=config['BOT']['TOKEN'])
# Диспетчер для бота
dp = Dispatcher(bot, storage=storage)
# База данных бота
database.create_tables()


# Хэндлер запуска
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await dp.bot.set_my_commands(ui.commands)  # Установка комманд
    user = database.find_user(message.from_user.id)
    if user is None:  # Проверка на регистрацию в боте
        database.add_user(message.from_user.id, message.from_user.full_name)
        await message.answer(ui.text_start_user_new.format(message.from_user.full_name), reply_markup=ui.keyboard_main)
    else:
        await message.answer(ui.text_start_user.format(message.from_user.full_name), reply_markup=ui.keyboard_main)


# Показ профиля
@dp.message_handler(Text(equals=ui.but_profile))
async def show_profile(message: types.Message):
    user = database.find_user(message.from_user.id)
    await message.answer(ui.text_profile.format(user[0], user[1], user[2]), reply_markup=ui.keyboard_main)


# Показ заданий
@dp.message_handler(Text(equals=ui.but_tasks))
async def show_tasks(message: types.Message):
    tasks = database.get_tasks()

    inline_tasks = InlineKeyboardMarkup()
    for task in tasks:
        inline_tasks.insert(
            InlineKeyboardButton(ui.text_tasks_line.format(task[1], task[2]), callback_data=f'taskshow_{task[0]}'))

    await message.answer(ui.text_tasks, reply_markup=inline_tasks)


# Хендлер показа задания
@dp.callback_query_handler(Text(startswith='taskshow'))
async def handle_task_show(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1])
    task = database.find_task(task_id)

    await bot.answer_callback_query(callback_query.id)

    keyboard_enter_flag = types.InlineKeyboardMarkup()
    keyboard_enter_flag.add(types.InlineKeyboardButton(ui.but_enter_flag, callback_data=f'flagenter_{task_id}'))

    if task:
        await bot.send_message(callback_query.from_user.id, ui.text_task.format(task[2], task[5], task[3]),
                               reply_markup=keyboard_enter_flag)


# Хендлер начала ввода флага
@dp.callback_query_handler(Text(startswith='flagenter'))
async def handle_flag_enter(callback_query: types.CallbackQuery):
    await UserStates.enter_flag.set()

    task_id = int(callback_query.data.split('_')[1])

    database.set_edit_task(callback_query.from_user.id, task_id)

    await bot.send_message(callback_query.from_user.id, ui.text_enter_flag)


# Хэндлер ввода флага
@dp.message_handler(state=UserStates.enter_flag)
async def enter_edit_task_name(message: types.Message, state: FSMContext):
    await state.finish()

    user = database.get_user_task_id(message.from_user.id)

    flag = database.find_task_flag(user)

    if message.text == flag:
        await message.answer(ui.text_flag_correct)
    else:
        await message.answer(ui.text_flag_incorrect)


# Отмена
@dp.message_handler(Text(equals=ui.but_cancel),
                    state=[UserStates.edit_name, UserStates.edit_desc, UserStates.edit_flag, UserStates.edit_points])
async def cancel_action(message: types.Message):
    await UserStates.edit.set()

    await message.answer(ui.text_cancel, reply_markup=ui.keyboard_admin)


# Возвращение назад
@dp.message_handler(Text(equals=ui.but_back), state=UserStates.all_states)
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(ui.text_back, reply_markup=ui.keyboard_main)


# Админ панель
@dp.message_handler(Text(equals=ui.but_admin))
async def show_admin_panel(message: types.Message):
    await UserStates.admin.set()

    await message.answer(ui.text_admin_panel, reply_markup=ui.keyboard_admin)


# Добавить задание
@dp.message_handler(Text(equals=ui.but_add_task), state=UserStates.admin)
async def show_add_task(message: types.Message):
    await UserStates.enter_add.set()

    await message.answer(ui.text_add_task, reply_markup=ui.keyboard_admin)


# Хэндлер ввода названия нового задания
@dp.message_handler(state=UserStates.enter_add)
async def enter_new_task(message: types.Message):
    await UserStates.admin.set()

    database.add_task(message.from_user.id, message.text)

    await message.answer(ui.text_task_added, reply_markup=ui.keyboard_admin)


# Изменить задание
@dp.message_handler(Text(equals=ui.but_edit_task), state=UserStates.admin)
async def show_edit_tasks(message: types.Message):
    await UserStates.edit_enter.set()

    tasks = database.get_tasks()
    text = ui.text_tasks
    for task in tasks:
        text += ui.text_edit_tasks_line.format(task[0], task[1])

    text += ui.text_edit_tasks

    await message.answer(text, reply_markup=ui.keyboard_admin)


# Показ изменяемого задания
async def show_edit_task(message: types.Message):
    text = ui.text_edit_task_entered.format(database.get_user_task_id(message.from_user.id))
    task = database.find_task(database.get_user_task_id(message.from_user.id))
    text += ui.text_task_full.format(task[2], task[5], task[3], task[4], task[1], bool(task[6]))

    await message.answer(text, reply_markup=ui.keyboard_edit_task)


# Хэндлер ввода изменения задания
@dp.message_handler(state=UserStates.edit_enter)
async def enter_edit_task(message: types.Message):
    task = database.find_task(message.text)

    if task:
        await UserStates.edit.set()

        database.set_edit_task(message.from_user.id, message.text)

        await show_edit_task(message)
    else:
        await message.answer(ui.text_edit_task_notentered.format(message.text), reply_markup=ui.keyboard_back)


# Показ ввода изменения названия задания
@dp.message_handler(Text(equals=ui.but_edit_name), state=UserStates.edit)
async def show_edit_task_name(message: types.Message):
    await UserStates.edit_name.set()

    await message.answer(ui.text_edit_name, reply_markup=ui.keyboard_back)


# Хэндлер ввода изменения названия задания
@dp.message_handler(state=UserStates.edit_name)
async def enter_edit_task_name(message: types.Message):
    await UserStates.edit.set()

    database.edit_task_name(database.get_user_task_id(message.from_user.id), message.text)

    await show_edit_task(message)


# Показ ввода изменения описания задания
@dp.message_handler(Text(equals=ui.but_edit_desc), state=UserStates.edit)
async def show_edit_task_desc(message: types.Message):
    await UserStates.edit_desc.set()

    await message.answer(ui.text_edit_desc, reply_markup=ui.keyboard_back)


# Хэндлер ввода изменения описания задания
@dp.message_handler(state=UserStates.edit_desc)
async def enter_edit_task_name(message: types.Message):
    await UserStates.edit.set()

    database.edit_task_desc(database.get_user_task_id(message.from_user.id), message.text)

    await show_edit_task(message)


# Показ ввода изменения флага задания
@dp.message_handler(Text(equals=ui.but_edit_flag), state=UserStates.edit)
async def show_edit_task_flag(message: types.Message):
    await UserStates.edit_flag.set()

    await message.answer(ui.text_edit_flag, reply_markup=ui.keyboard_back)


# Хэндлер ввода изменения флага задания
@dp.message_handler(state=UserStates.edit_flag)
async def enter_edit_task_flag(message: types.Message):
    await UserStates.edit.set()

    database.edit_task_flag(database.get_user_task_id(message.from_user.id), message.text)

    await show_edit_task(message)


# Показ ввода изменения очков задания
@dp.message_handler(Text(equals=ui.but_edit_points), state=UserStates.edit)
async def show_edit_task_points(message: types.Message):
    await UserStates.edit_points.set()

    await message.answer(ui.text_edit_points, reply_markup=ui.keyboard_back)


# Хэндлер ввода изменения очков задания
@dp.message_handler(state=UserStates.edit_points)
async def enter_edit_task_points(message: types.Message):
    await UserStates.edit.set()

    database.edit_task_points(database.get_user_task_id(message.from_user.id), message.text)

    await show_edit_task(message)


# Удалить задание
@dp.message_handler(Text(equals=ui.but_delete_task), state=UserStates.edit)
async def show_delete_task(message: types.Message):
    await UserStates.admin.set()

    database.delete_task(database.get_user_task_id(message.from_user.id))

    await message.answer(ui.text_task_deleted, reply_markup=ui.keyboard_admin)


def start_bot():  # Запуск бота
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    start_bot()
