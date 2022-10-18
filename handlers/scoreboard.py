from bot import dp, bot, UserStates
import database
import ui
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


# Хэндлер показа рейтинга
@dp.message_handler(commands='score')
@dp.message_handler(Text(equals=ui.BUT_SCOREBOARD))
async def show_scoreboard(message: types.Message):
    scoreboard = database.get_scoreboard()

    text = ui.TEXT_SCOREBOARD
    pos = 0
    for score in scoreboard:
        pos += 1
        text += ui.TEXT_SCOREBOARD_LINE.format(position=pos, name=score['username'], score=score['score'])

    await message.answer(text)