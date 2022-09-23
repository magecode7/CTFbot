from aiogram import types

# Кнопки
but_profile = 'Профиль'
but_tasks = 'Задания'
but_scoreboard = 'Рейтинг'
but_admin = 'Админ-панель'
but_back = 'Назад'
but_cancel = 'Отмена'

but_edit_name = 'Изменить имя'
but_edit_desc = 'Изменить описание'
but_edit_flag = 'Изменить флаг'
but_edit_points = 'Изменить кол-во очков'

but_add_task = 'Добавить задание'
but_edit_task = 'Изменить задание'
but_delete_task = 'Удалить задание'

but_enter_flag = 'Ввести флаг'

# Тексты
text_start_user = 'Привет, {0}, добро пожаловать на CTF'
text_start_user_new = 'Привет, новый пользователь {0}, добро пожаловать на CTF'
text_profile = 'ID пользователя: {0}\nИмя пользователя: {1}\nКоличество очков: {2}'
text_admin_panel = 'Админ панель открыта'
text_add_task = 'Введите название нового задания:'
text_cancel = 'Отмена'
text_back = 'Возвращение в меню'
text_task_added = 'Задание добавлено'
text_task_deleted = 'Задание удалено'
text_tasks = 'Задания:'
text_tasks_line = '{0} ({1})'
text_edit_tasks = '\nВведите ID задания которое вы хотите изменить'
text_edit_tasks_line = '{0}) {1}\n'
text_edit_task_entered = 'Выбрано задание ID {0}'
text_edit_task_notentered = 'Задания с ID {0} не существует!'
text_task_full = '\n\n{0}\n\nОчки: {1}\n\nОписание:\n{2}\n\nФлаг: {3}\nВладелец: {4}\nВидимость: {5}'
text_task = '{0} ({1})\n\n{2}'
text_edit_name = 'Ввведите новое имя:'
text_edit_desc = 'Введите новое описание:'
text_edit_flag = 'Введите новый флаг:'
text_edit_points = 'Введите новое значение очков:'
text_enter_flag = 'Введите флаг:'
text_flag_correct = 'Верно!'
text_flag_incorrect = 'Неверно!'

# Команды
commands = [
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('help', 'Помощь')
    ]

# Клавиатура бота
keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(*[but_profile, but_tasks, but_scoreboard, but_admin])

keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_admin.add(*[but_add_task, but_edit_task, but_back])

keyboard_edit_task = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_edit_task.add(*[but_edit_name, but_edit_desc, but_edit_flag, but_edit_points, but_delete_task, but_back])

keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_back.add(*[but_back])




