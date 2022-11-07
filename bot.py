import logging
import config
import database
import ui
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


# Логирование
# logging.basicConfig(filename='bot.log', level=logging.DEBUG)
# Хранилище состояний
storage = MemoryStorage()
# Бот токен
bot = Bot(token=config.TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot, storage=storage)
# База данных бота
database.create_tables()
if not database.get_user(config.ADMIN):
    database.add_user(config.ADMIN, 'admin', 5)


# Состояния
class BotStates(StatesGroup):
    admin = State()
    user_change_name = State()
    task_add_enter = State()
    task_edit = State()
    task_edit_enter = State()
    task_edit_name = State()
    task_edit_desc = State()
    task_edit_flag = State()
    task_edit_points = State()
    task_file_add = State()
    task_flag_enter = State()
    user_edit = State()
    user_edit_name = State()
    user_edit_rights = State()
    broadcast_enter = State()
    database_query_enter = State()
    time_start_set = State()


# При включении
async def on_startup(dp):
    await bot.send_message(config.ADMIN, ui.TEXT_BOT_STARTUP)


# При отключении
async def on_shutdown(dp):
    await bot.send_message(config.ADMIN, ui.TEXT_BOT_SHUTDOWN)


def start_bot():  # Запуск бота
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
    start_bot()
