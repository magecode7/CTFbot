import database
import ui
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class RightsFilter(BoundFilter):
    key = 'min_rights'

    def __init__(self, min_rights: int):
        self.min_rights = min_rights
    

    async def check(self, message: types.Message) -> bool:
        check = database.get_user_rights(message.from_user.id) >= self.min_rights

        if not check: await message.answer(ui.TEXT_RIGHTS_MISSED)

        return check
