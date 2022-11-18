from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import database
import ui
from bot import BotStates, bot, dp, logger


# Показ профиля
@dp.message_handler(commands='profile')
@dp.message_handler(Text(equals=ui.BUT_PROFILE))
async def show_profile(message: types.Message):
    user = database.get_user(message.from_user.id)

    inline_profile = types.InlineKeyboardMarkup()
    inline_profile.add(types.InlineKeyboardButton(
        ui.BUT_USER_NAME_CHANGE, callback_data=f'changename_{message.from_user.id}'))

    if user:
        await message.answer(ui.TEXT_USER_PROFILE.format(id=user['id'], name=user['name'], points=database.get_user_score(message.from_user.id)), parse_mode='html', reply_markup=inline_profile)
    else:
        await message.answer(ui.TEXT_USER_UNREGISTER)


# Хендлер изменения имени
@dp.callback_query_handler(Text(startswith='changename'))
async def handle_profile_change_name(callback_query: types.CallbackQuery):
    await BotStates.user_change_name.set()

    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, ui.TEXT_USER_NAME_CHANGE, reply_markup=ui.keyboard_back)


# Хэндлер ввода нового имени
@dp.message_handler(state=BotStates.user_change_name)
async def enter_edit_task_name(message: types.Message, state: FSMContext):
    if len(message.text) > 16:
        await message.answer(ui.TEXT_USER_NAME_CHANGE_OUTBOUND)
        return

    await state.finish()

    database.set_user_name(message.from_user.id, message.text)

    logger.info(f'User \"{message.from_user.full_name}\" ({message.from_user.id}) changed username to \"{message.text}\"')

    await message.answer(ui.TEXT_USER_NAME_CHANGED, reply_markup=ui.keyboard_main)
    await show_profile(message)
