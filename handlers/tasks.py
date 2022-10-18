from bot import dp, bot, UserStates
import database
import ui
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


# Показ заданий
@dp.message_handler(commands='tasks')
@dp.message_handler(Text(equals=ui.BUT_TASKS))
async def show_tasks(message: types.Message):
    if database.get_user_block(message.from_user.id):
        await message.answer(ui.TEXT_YOU_ARE_BLOCKED)
        return

    tasks = database.get_tasks()

    inline_tasks = types.InlineKeyboardMarkup()
    for task in tasks:
        visible = task['visible']
        if visible:
            inline_tasks.insert(types.InlineKeyboardButton(ui.TEXT_TASKS_LINE.format(name=task['name'], points=task['points']), callback_data=f"taskshow_{task['id']}"))

    await message.answer(ui.TEXT_TASKS, reply_markup=inline_tasks)


# Хендлер показа задания
@dp.callback_query_handler(Text(startswith='taskshow'))
async def handle_task_show(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1])
    task = database.get_task(task_id)

    inline_keyboard_task = types.InlineKeyboardMarkup()
    solved = database.get_task_solved(callback_query.from_user.id, task_id)
    if not solved: 
        inline_keyboard_task.insert(types.InlineKeyboardButton(ui.BUT_TASK_FLAG_ENTER, callback_data=f'flagenter_{task_id}'))
    
    files = database.get_files(task_id)
    if files:
        inline_keyboard_task.insert(types.InlineKeyboardButton(ui.BUT_TASK_FILES.format(count=len(files)), callback_data=f'taskfiles_{task_id}'))

    await callback_query.answer()

    if task:
        await bot.send_message(callback_query.from_user.id, ui.TEXT_TASK.format(name=task['name'], points=task['points'], desc=task['description']) + (ui.TEXT_TASK_SOLVED if solved else ''), reply_markup=inline_keyboard_task)


# Хендлер прикрепленных файлов
@dp.callback_query_handler(Text(startswith='taskfiles'))
async def handle_flag(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1])

    files = database.get_files(task_id)
    media = types.MediaGroup()
    for file in files:
        media.attach_document(types.InputMediaDocument(file['path']))

    await callback_query.answer()
    await bot.send_media_group(callback_query.from_user.id, media)


# Хендлер начала ввода флага
@dp.callback_query_handler(Text(startswith='flagenter'))
async def handle_flag_enter(callback_query: types.CallbackQuery):
    await UserStates.task_flag_enter.set()

    task_id = int(callback_query.data.split('_')[1])

    database.set_selected_task(callback_query.from_user.id, task_id)

    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, ui.TEXT_TASK_FLAG_CHECK, reply_markup=types.ReplyKeyboardRemove())


# Хэндлер ввода флага
@dp.message_handler(state=UserStates.task_flag_enter)
async def enter_edit_task_name(message: types.Message, state: FSMContext):
    await state.finish()

    task_id = database.get_selected_task_id(message.from_user.id)

    flag = database.get_task_flag(task_id)

    if message.text == flag:
        database.add_solve(message.from_user.id, task_id)

        await message.answer(ui.TEXT_TASK_FLAG_CORRECT, reply_markup=ui.keyboard_main)
    else:
        await message.answer(ui.TEXT_TASK_FLAG_INCORRECT, reply_markup=ui.keyboard_main)