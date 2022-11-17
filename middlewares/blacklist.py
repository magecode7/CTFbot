import database
import ui

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware


def blacklist_ignore(access=False):
    def decorator(func):
        setattr(func, 'blacklist_access', access)
        return func

    return decorator


class BlacklistMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, access=False):
        self.access = access
        super(BlacklistMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        if handler:
            access = getattr(handler, 'blacklist_access', self.access)
        else:
            access = self.access

        blocked = database.get_user_block(message.from_user.id)

        if blocked and not access:
            await message.answer(ui.TEXT_YOU_ARE_BLOCKED)

            raise CancelHandler()
