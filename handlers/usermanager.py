from bot import dp, bot, BotStates
import database
import ui
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


# Показ изменяемого пользователя
async def show_editable_user(user_id: int):
    text = ui.TEXT_USER_SELECTED.format(id=user_id)

    user = database.get_user(database.get_selected_user_id(user_id))
    text += ui.TEXT_USER_EDITING.format(name=user['name'], rights=user['rights'], blocked=bool(user['blocked']))

    await bot.send_message(user_id, text, reply_markup=ui.keyboard_edit_user)


# Хэндлер ввода изменения пользователя
@dp.callback_query_handler(Text(startswith='useredit'), state=BotStates.admin)
async def user_edit_handle(callback_query: types.CallbackQuery):
    rights = database.get_user_rights(callback_query.from_user.id)
    selected_user_id = int(callback_query.data.split('_')[1])
    selected_user = database.get_user(selected_user_id)

    await bot.answer_callback_query(callback_query.id)

    if rights < 3 or selected_user['rights'] >= rights:
        await bot.send_message(callback_query.from_user.id, ui.TEXT_RIGHTS_MISSED)
        return

    if selected_user:
        database.set_selected_user(callback_query.from_user.id, selected_user_id)

        await BotStates.user_edit.set()

        await show_editable_user(callback_query.from_user.id)
    else:
        await bot.send_message(callback_query.from_user.id, ui.TEXT_USER_MISSED, reply_markup=ui.keyboard_back)


# Показ ввода изменения имени пользователя
@dp.message_handler(Text(equals=ui.BUT_USER_NAME_EDIT), state=BotStates.user_edit)
async def show_edit_user_name(message: types.Message):
    await BotStates.user_edit_name.set()

    await message.answer(ui.TEXT_USER_NAME_EDIT, reply_markup=ui.keyboard_back)


# Перехватчик ввода изменения имени пользователя
@dp.message_handler(state=BotStates.user_edit_name)
async def enter_edit_user_name(message: types.Message):
    await BotStates.user_edit.set()

    database.set_user_name(database.get_selected_user_id(message.from_user.id), message.text)

    await show_editable_user(message.from_user.id)


# Показ ввода изменения прав пользователя
@dp.message_handler(Text(equals=ui.BUT_USER_RIGHTS_EDIT), state=BotStates.user_edit)
async def show_edit_user_rights(message: types.Message):
    await BotStates.user_edit_rights.set()

    await message.answer(ui.TEXT_USER_RIGHTS_EDIT, reply_markup=ui.keyboard_back)


# Перехватчик ввода изменения прав пользователя
@dp.message_handler(state=BotStates.user_edit_rights)
async def enter_edit_user_rights(message: types.Message):   
    selected_user_id = database.get_selected_user_id(message.from_user.id)
    old_rights = database.get_user_rights(selected_user_id)

    try:
        rights = int(message.text)

        if old_rights >= rights:
            await message.answer(ui.TEXT_USER_RIGHTS_LEVEL_REQUERED)
            return

        if rights < 0 or rights > 4:
            await message.answer(ui.TEXT_USER_RIGHTS_NOT_DIGIT)
            return
        
        database.set_user_rights(selected_user_id, rights)

        await BotStates.user_edit.set()

        await show_editable_user(message.from_user.id)

    except Exception:
        await message.answer(ui.TEXT_USER_RIGHTS_NOT_DIGIT)


# Изменение блокировки пользователя
@dp.message_handler(Text(equals=ui.BUT_USER_BLOCK_EDIT), state=BotStates.user_edit)
async def show_edit_user_block(message: types.Message):
    selected_user_id = database.get_selected_user_id(message.from_user.id)

    user = database.get_user(selected_user_id)
    blocked = user['blocked']

    database.set_user_block(selected_user_id, not blocked)

    if blocked: await message.answer(ui.TEXT_USER_UNBLOCKED)
    else: await message.answer(ui.TEXT_USER_BLOCKED)

    await show_editable_user(message.from_user.id)