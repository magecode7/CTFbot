from aiogram import types

# Кнопки меню
BUT_PROFILE = 'Профиль'
BUT_TASKS = 'Задания'
BUT_SCOREBOARD = 'Рейтинг'
BUT_ADMIN_MENU = 'Админ-меню'
BUT_BACK = 'Назад'
BUT_CANCEL = 'Отмена'
# Кнопки админ-меню
BUT_TASK_ADD = 'Добавить задание'
BUT_TASK_EDIT = 'Изменить задание'
BUT_USER_EDIT = 'Изменить пользователя'
# Кнопки редактора задания
BUT_TASK_NAME_EDIT = 'Изменить имя'
BUT_TASK_DESC_EDIT = 'Изменить описание'
BUT_TASK_FLAG_EDIT = 'Изменить флаг'
BUT_TASK_POINTS_EDIT = 'Изменить кол-во очков'
BUT_TASK_VISIBILITY_EDIT = 'Изменить видимость'
BUT_TASK_FILE_ADD = 'Добавить файл'
BUT_TASK_FILE_DELETE = 'Удалить файл'
BUT_TASK_RESET = 'Сбросить решения'
BUT_TASK_DELETE = 'Удалить задание'
# Кнопки редактора пользователей
BUT_USER_NAME_EDIT = 'Изменить имя'
BUT_USER_RIGHTS_EDIT = 'Изменить права'
BUT_USER_BLOCK_EDIT = 'Изменить блокировку'
# Кнопки задания
BUT_TASK_FLAG_ENTER = 'Ввести флаг'
BUT_TASK_FILES = 'Прикрепленные файлы ({count})'
# Кнопки профиля
BUT_USER_NAME_CHANGE = 'Изменить имя'
# Тексты меню
TEXT_USER_START = '{username}, добро пожаловать на KrduCTF!\n{time}'
TEXT_USER_MISSED = 'Пользователь не найден!'
TEXT_USER_START_NEW = '{username}, вы были зарегистрированы, добро пожаловать на KrduCTF!{time}'
TEXT_USER_UNREGISTER = 'Вы не зарегистрированы в боте, пожалуйста, введите /start'
TEXT_ADMIN_MENU_OPENED = 'Админ-меню открыто'
TEXT_HELP = '''
МЕНЮ ПОМОЩИ\n
CTF (Capture the flag или Захват флага) — командные соревнования в области компьютерной (информационной) безопасности.\n
Task-based (или jeopardy) — игрокам предоставляется набор тасков (заданий), к которым требуется найти ответ (флаг) и отправить его.\n
Данный бот разработан <code>@magecode</code>
'''
# Тексты админ-меню
TEXT_TASK_ADD = 'Введите название нового задания:'
TEXT_CANCEL = 'Отменяем...'
TEXT_BACK = 'Возвращение в меню...'
TEXT_TASK_ADDED = 'Задание добавлено'
TEXT_TASK_DELETED = 'Задание удалено'
TEXT_RIGHTS_MISSED = 'Недостаточно прав'
TEXT_YOU_ARE_BLOCKED = 'Вы заблокированы!'
# Тексты редактора заданий
TEXT_TASKS = 'ЗАДАНИЯ'
TEXT_TASKS_LINE = '{name} ({points})'
TEXT_TASK_SELECTED = 'Выбрано задание ID {id}'
TEXT_TASK_MISSED = 'Задание не найдено!'
TEXT_TASK_EDITING = '\n\n{name}\n\nОчки: {points}\n\nОписание:\n{desc}\n\nФлаг: {flag}\nВладелец: {owner}\nВидимость: {visible}\n\nФайлы:'
TEXT_TASK_NAME_EDIT = 'Ввведите новое имя:'
TEXT_TASK_DESC_EDIT = 'Введите новое описание:'
TEXT_TASK_FLAG_EDIT = 'Введите новый флаг:'
TEXT_TASK_POINTS_EDIT = 'Введите новое значение очков:'
TEXT_TASK_POINTS_EDIT_ERROR = 'Введите корректное значение!'
TEXT_TASK_FILE_ADD = 'Прикрепите файл:'
TEXT_TASK_FILE_ADDED = 'Файл прикреплен'
TEXT_TASK_FILES_MISSED = 'Нет прикреплённых файлов!'
TEXT_TASK_FILES_DELETE = 'Выберите какой файл хотите удалить:'
TEXT_TASK_FILE_DELETED = 'Файл удалён!'
TEXT_TASK_RESETED = 'Решения сброшены!'
# Тексты редактора пользователей
TEXT_USERS = 'ПОЛЬЗОВАТЕЛИ'
TEXT_USERS_LINE = '#{id} - {name}'
TEXT_USER_SELECTED = 'Выбран пользователь ID {id}'
TEXT_USER_EDITING = '\n\n{name}\n\nПолномочия: {rights}\n\nБлокировка: {blocked}'
TEXT_USER_NAME_EDIT = 'Введите новое имя:'
TEXT_USER_RIGHTS_EDIT = '''
Введите уровень прав, где:
0 - нет прав
1 - доступ к своим заданиям
2 - доступ ко всем заданиям
3 - прошлый уровень + доступ к пользователям
4 - полный доступ

Нельзя назначить такие же права как у вас или выше!
'''
TEXT_USER_RIGHTS_NOT_DIGIT = 'Введите корректное число от 0 до 4!'
TEXT_USER_RIGHTS_LEVEL_REQUERED = 'Невозможно указать права своего уровня и выше!'
TEXT_USER_BLOCKED = 'Пользователь заблокирован'
TEXT_USER_UNBLOCKED = 'Пользователь разблокирован'
# Тексты рейтинга
TEXT_SCOREBOARD = 'РЕЙТИНГ УЧАСТНИКОВ'
TEXT_SCOREBOARD_LINE = '\n#{position} {name} - {score}'
# Тексты меню задания
TEXT_TASK = '{name} ({points})\n\n{desc}'
TEXT_TASK_FLAG_CHECK = 'Введите флаг:'
TEXT_TASK_FLAG_CORRECT = 'Верно!'
TEXT_TASK_FLAG_INCORRECT = 'Неверно!'
TEXT_TASK_SOLVED = '\n\nЗадание уже решено'
# Тексты профиля
TEXT_USER_PROFILE = 'ПРОФИЛЬ\nID пользователя: <code>{id}</code>\nИмя пользователя: {name}\nКоличество очков: {points}'
TEXT_USER_NAME_CHANGE = 'Введите новое имя:'
TEXT_USER_NAME_CHANGED = 'Имя изменено'

# Команды
commands = [
    types.BotCommand('start', 'Запустить бота'),
    types.BotCommand('help', 'Помощь'),
    types.BotCommand('profile', 'Открыть профиль'),
    types.BotCommand('tasks', 'Открыть задания'),
    types.BotCommand('score', 'Открыть рейтинг'),
    types.BotCommand('back', 'Возвращает назад')
]

# Клавиатура бота
keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(*[BUT_PROFILE, BUT_TASKS, BUT_SCOREBOARD])

keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_admin.row(*[BUT_TASK_ADD, BUT_TASK_EDIT])
keyboard_admin.row(BUT_USER_EDIT)
keyboard_admin.row(BUT_BACK)

keyboard_edit_task = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_edit_task.row(BUT_TASK_VISIBILITY_EDIT)
keyboard_edit_task.row(*[BUT_TASK_NAME_EDIT, BUT_TASK_DESC_EDIT, BUT_TASK_FLAG_EDIT, BUT_TASK_POINTS_EDIT])
keyboard_edit_task.row(*[BUT_TASK_FILE_ADD, BUT_TASK_FILE_DELETE])
keyboard_edit_task.row(*[BUT_TASK_RESET , BUT_TASK_DELETE])
keyboard_edit_task.row(BUT_BACK)

keyboard_edit_user = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_edit_user.row(BUT_USER_NAME_EDIT)
keyboard_edit_user.row(*[BUT_USER_RIGHTS_EDIT, BUT_USER_BLOCK_EDIT])
keyboard_edit_user.row(BUT_BACK)

keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back.add(*[BUT_BACK])