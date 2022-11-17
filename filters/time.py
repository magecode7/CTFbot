from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import database
import datetime
import ui


class StartTimeFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        start_time = database.get_start_time()
        if not start_time:
            return True

        is_started = start_time < datetime.datetime.now()

        if not is_started:
            await message.answer(ui.TEXT_MAIN_NOT_STARTED)

        return is_started


class EndTimeFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        end_time = database.get_end_time()
        if not end_time:
            return True

        is_ended = end_time < datetime.datetime.now()

        if is_ended:
            await message.answer(ui.TEXT_MAIN_ENDED)

        return not is_ended
