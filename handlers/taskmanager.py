from aiogram import types
from aiogram.dispatcher.filters import Text
from filters.rights import MinRightsFilter

import database
import ui
from bot import BotStates, bot, dp


# Показ изменяемого задания
async def show_editable_task(user_id: int):
    text = ui.TEXT_TASK_SELECTED.format(
        id=database.get_selected_task_id(user_id))

    task = database.get_task(database.get_selected_task_id(user_id))
    text += ui.TEXT_TASK_EDITING.format(name=task['name'], points=task['points'], desc=task['description'],
                                        flag=task['flag'], owner=task['owner_user_id'], visible=bool(task['visible']))

    files = database.get_files(task['id'])
    if files:
        counter = 0
        for file in files:
            counter += 1
            text += f'\n#{counter} ' + file[3]
    else:
        text += ui.TEXT_TASK_FILES_MISSED

    await bot.send_message(user_id, text, reply_markup=ui.keyboard_edit_task)


# Хэндлер ввода изменения задания
@dp.callback_query_handler(Text(startswith='taskedit'), MinRightsFilter(1), state=BotStates.admin)
async def task_edit_handle(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1])
    task = database.get_task(task_id)

    await bot.answer_callback_query(callback_query.id)

    if task['owner_user_id'] != callback_query.from_user.id and database.get_user_rights(callback_query.from_user.id) <= 1:
        await bot.send_message(callback_query.from_user.id, ui.TEXT_RIGHTS_MISSED)
        return

    if task:
        database.set_selected_task(callback_query.from_user.id, task_id)

        await BotStates.task_edit.set()

        await show_editable_task(callback_query.from_user.id)
    else:
        await bot.send_message(callback_query.from_user.id, ui.TEXT_TASK_MISSED, reply_markup=ui.keyboard_back)


# Показ ввода изменения названия задания
@dp.message_handler(Text(equals=ui.BUT_TASK_NAME_EDIT), state=BotStates.task_edit)
async def show_edit_task_name(message: types.Message):
    await BotStates.task_edit_name.set()

    await message.answer(ui.TEXT_TASK_NAME_EDIT, reply_markup=ui.keyboard_back)


# Перехватчик ввода изменения названия задания
@dp.message_handler(state=BotStates.task_edit_name)
async def enter_edit_task_name(message: types.Message):
    if len(message.text) > 16:
        await message.answer(ui.TEXT_TASK_NAME_EDIT_OUTBOUND)
        return

    database.set_task_name(database.get_selected_task_id(
        message.from_user.id), message.text)

    await BotStates.task_edit.set()

    await show_editable_task(message.from_user.id)


# Показ ввода изменения описания задания
@dp.message_handler(Text(equals=ui.BUT_TASK_DESC_EDIT), state=BotStates.task_edit)
async def show_edit_task_desc(message: types.Message):
    await BotStates.task_edit_desc.set()

    await message.answer(ui.TEXT_TASK_DESC_EDIT, reply_markup=ui.keyboard_back)


# Перехватчик ввода изменения описания задания
@dp.message_handler(state=BotStates.task_edit_desc)
async def enter_edit_task_desc(message: types.Message):
    if len(message.text) > 256:
        await message.answer(ui.TEXT_TASK_DESC_EDIT_OUTBOUND)
        return

    database.set_task_desc(database.get_selected_task_id(
        message.from_user.id), message.text)

    await BotStates.task_edit.set()

    await show_editable_task(message.from_user.id)


# Показ ввода изменения флага задания
@dp.message_handler(Text(equals=ui.BUT_TASK_FLAG_EDIT), state=BotStates.task_edit)
async def show_edit_task_flag(message: types.Message):
    await BotStates.task_edit_flag.set()

    await message.answer(ui.TEXT_TASK_FLAG_EDIT, reply_markup=ui.keyboard_back)


# Перехватчик ввода изменения флага задания
@dp.message_handler(state=BotStates.task_edit_flag)
async def enter_edit_task_flag(message: types.Message):
    if len(message.text) > 32:
        await message.answer(ui.TEXT_TASK_FLAG_EDIT_OUTBOUND)
        return

    database.set_task_flag(database.get_selected_task_id(
        message.from_user.id), message.text)

    await BotStates.task_edit.set()

    await show_editable_task(message.from_user.id)


# Показ ввода изменения очков задания
@dp.message_handler(Text(equals=ui.BUT_TASK_POINTS_EDIT), state=BotStates.task_edit)
async def show_edit_task_points(message: types.Message):
    await BotStates.task_edit_points.set()

    await message.answer(ui.TEXT_TASK_POINTS_EDIT, reply_markup=ui.keyboard_back)


# Перехватчик ввода изменения очков задания
@dp.message_handler(state=BotStates.task_edit_points)
async def enter_edit_task_points(message: types.Message):
    try:
        points = int(message.text)

        if points < 0 or points > 1000:
            await message.answer(ui.TEXT_TASK_POINTS_EDIT_OUTBOUND)
            return

        database.set_task_points(
            database.get_selected_task_id(message.from_user.id), points)

        await BotStates.task_edit.set()

        await show_editable_task(message.from_user.id)
    except Exception as e:
        await message.answer(ui.TEXT_TASK_POINTS_EDIT_ERROR)


# Изменение видимости задания
@dp.message_handler(Text(equals=ui.BUT_TASK_VISIBILITY_EDIT), state=BotStates.task_edit)
async def show_edit_task_visibile(message: types.Message):
    selected_task_id = database.get_selected_task_id(message.from_user.id)

    task = database.get_task(selected_task_id)

    database.set_task_visibility(selected_task_id, not task['visible'])

    await show_editable_task(message.from_user.id)


# Удалить задание
@dp.message_handler(Text(equals=ui.BUT_TASK_DELETE), state=BotStates.task_edit)
async def show_delete_task(message: types.Message):
    database.delete_task(database.get_selected_task_id(message.from_user.id))

    await BotStates.admin.set()

    await message.answer(ui.TEXT_TASK_DELETED, reply_markup=ui.keyboard_admin)


# Добавить файл к заданию
@dp.message_handler(Text(equals=ui.BUT_TASK_FILE_ADD), state=BotStates.task_edit)
async def file_add(message: types.Message):
    files = database.get_files(
        database.get_selected_task_id(message.from_user.id))

    if len(files) >= 5:
        await message.answer(ui.TEXT_TASK_FILE_ADD_UNBOUND)
        return

    await BotStates.task_file_add.set()

    await message.answer(ui.TEXT_TASK_FILE_ADD, reply_markup=ui.keyboard_back)


# Перехватчик файла
@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=BotStates.task_file_add)
async def file_handle(message: types.Message):
    database.add_file(database.get_selected_task_id(
        message.from_user.id), message.document.file_id,  message.document.file_name)

    await BotStates.task_edit.set()

    await message.answer(ui.TEXT_TASK_FILE_ADDED)

    await show_editable_task(message.from_user.id)


# Удаление файлов
@dp.message_handler(Text(equals=ui.BUT_TASK_FILE_DELETE), state=BotStates.task_edit)
async def file_delete(message: types.Message):
    task_id = database.get_selected_task_id(message.from_user.id)

    files = database.get_files(task_id)

    inline_files = types.InlineKeyboardMarkup()
    for file in files:
        inline_files.add(types.InlineKeyboardButton(
            file['name'], callback_data=f"filedelete_{file['id']}_{task_id}"))

    await message.answer(ui.TEXT_TASK_FILES_DELETE, reply_markup=inline_files)


# Перехват удаления файла
@dp.callback_query_handler(Text(startswith='filedelete'), state=BotStates.task_edit)
async def handle_file_delete(callback_query: types.CallbackQuery):
    file_id = int(callback_query.data.split('_')[1])
    task_id = int(callback_query.data.split('_')[2])

    database.delete_file(file_id)

    files = database.get_files(task_id)

    inline_files = types.InlineKeyboardMarkup()
    for file in files:
        inline_files.add(types.InlineKeyboardButton(
            file['name'], callback_data=f"filedelete_{file['id']}_{task_id}"))

    await callback_query.answer()
    if files:
        await callback_query.message.edit_reply_markup(inline_files)
    else:
        await callback_query.message.delete()
    await callback_query.message.answer(ui.TEXT_TASK_FILE_DELETED)
    await show_editable_task(callback_query.from_user.id)


# Сбросить решения задания
@dp.message_handler(Text(equals=ui.BUT_TASK_RESET), state=BotStates.task_edit)
async def task_reset_solves(message: types.Message):
    database.reset_task(database.get_selected_task_id(message.from_user.id))

    await message.answer(ui.TEXT_TASK_RESETED)
