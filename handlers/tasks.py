from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from filters.time import StartTimeFilter, EndTimeFilter

import database
import ui
from bot import BotStates, bot, dp, logger


# Показ заданий
@dp.message_handler(StartTimeFilter(), EndTimeFilter(), commands='tasks')
@dp.message_handler(Text(equals=ui.BUT_TASKS), StartTimeFilter())
async def show_tasks(message: types.Message):
    if database.get_user_block(message.from_user.id):
        await message.answer(ui.TEXT_YOU_ARE_BLOCKED)
        return

    tasks = database.get_tasks()

    inline_tasks = types.InlineKeyboardMarkup()
    for task in tasks:
        visible = task['visible']
        if visible:
            inline_tasks.insert(types.InlineKeyboardButton(ui.TEXT_TASKS_LINE.format(
                name=task['name'], points=task['points']), callback_data=f"taskshow_{task['id']}"))

    await message.answer(ui.TEXT_TASKS, reply_markup=inline_tasks)


# Хендлер показа задания
@dp.callback_query_handler(Text(startswith='taskshow'), StartTimeFilter())
async def handle_task_show(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1])
    task = database.get_task(task_id)

    inline_keyboard_task = types.InlineKeyboardMarkup()
    solved = database.get_task_solved_by(callback_query.from_user.id, task_id)
    if not solved:
        inline_keyboard_task.insert(types.InlineKeyboardButton(
            ui.BUT_TASK_FLAG_ENTER, callback_data=f'flagenter_{task_id}'))

    files = database.get_files(task_id)
    if files:
        inline_keyboard_task.insert(types.InlineKeyboardButton(
            ui.BUT_TASK_FILES.format(count=len(files)), callback_data=f'taskfiles_{task_id}'))

    solves = database.get_task_solves(task_id)
    if solves:
            inline_keyboard_task.insert(types.InlineKeyboardButton(
                ui.BUT_TASK_SOLVES.format(count=len(solves)), callback_data=f'tasksolves_{task_id}'))

    await callback_query.answer()

    if task:
        await bot.send_message(callback_query.from_user.id, ui.TEXT_TASK.format(name=task['name'], points=task['points'], desc=task['description']) + (ui.TEXT_TASK_SOLVED if solved else ''), reply_markup=inline_keyboard_task)


# Хендлер показа решений
@dp.callback_query_handler(Text(startswith='tasksolves'), StartTimeFilter())
async def handle_task_solves(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1])
    solves = database.get_task_solves(task_id)
    num = 0
    text = ui.TEXT_TASK_SOLVES
    for solve in solves:
        num += 1
        text += ui.TEXT_TASK_SOLVES_LINE.format(num=num, username=solve['username'])

    await bot.send_message(callback_query.from_user.id, text)


# Хендлер прикрепленных файлов
@dp.callback_query_handler(Text(startswith='taskfiles'), StartTimeFilter())
async def handle_task_files(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1])

    files = database.get_files(task_id)
    media = types.MediaGroup()
    for file in files:
        media.attach_document(types.InputMediaDocument(file['path']))

    await callback_query.answer()
    await bot.send_media_group(callback_query.from_user.id, media)


# Хендлер начала ввода флага
@dp.callback_query_handler(Text(startswith='flagenter'), StartTimeFilter(), EndTimeFilter())
async def handle_flag_enter(callback_query: types.CallbackQuery):
    await BotStates.task_flag_enter.set()

    task_id = int(callback_query.data.split('_')[1])

    database.set_selected_task(callback_query.from_user.id, task_id)

    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, ui.TEXT_TASK_FLAG_CHECK, reply_markup=ui.keyboard_back)


# Хэндлер ввода флага
@dp.message_handler(StartTimeFilter(), EndTimeFilter(), state=BotStates.task_flag_enter)
async def enter_edit_task_name(message: types.Message, state: FSMContext):
    task_id = database.get_selected_task_id(message.from_user.id)

    flag = database.get_task_flag(task_id)

    if message.text == flag:
        logger.info(f'User \"{message.from_user.full_name}\" ({message.from_user.id}) enter a CORRECT flag: \"{flag}\"')

        await state.finish()

        database.add_solve(message.from_user.id, task_id)

        await message.answer(ui.TEXT_TASK_FLAG_CORRECT, reply_markup=ui.keyboard_main)
    else:
        logger.info(f'User \"{message.from_user.full_name}\" ({message.from_user.id}) enter an INCORRECT flag: \"{flag}\"')

        await message.answer(ui.TEXT_TASK_FLAG_INCORRECT)
