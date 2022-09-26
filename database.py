import sqlite3

conn = sqlite3.connect("bot.db")
cur = conn.cursor()


def create_tables():
    """Инициирует таблицы если они еще не были созданы"""

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        admin INTEGER DEFAULT 0,
        selected_task_id INTEGER,
        FOREIGN KEY (selected_task_id) REFERENCES tasks (id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT DEFAULT '',
        flag TEXT DEFAULT '',
        points INTEGER DEFAULT 0,
        visible INTEGER DEFAULT 0,
        FOREIGN KEY (owner_user_id) REFERENCES users (id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS solves(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS file_paths(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        path TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )""")
    conn.commit()


def get_user(user_id: int) -> tuple:
    """Возвращает данные пользователя (id, name, admin, selected_task_id)"""

    cur.execute("SELECT * FROM users WHERE id = ?", (user_id, ))

    return cur.fetchone()


def get_task(task_id: int) -> tuple:
    """Возвращает данные задания (id, owner_user_id, name, description, flag, points, visible)"""

    cur.execute("SELECT * FROM tasks  WHERE id = ?", (task_id, ))
    return cur.fetchone()


def get_task_flag(task_id: int) -> str:
    """Возвращает флаг-ключ задания"""

    cur.execute("SELECT flag FROM tasks WHERE id = ?", (task_id, ))
    return str(cur.fetchone()[0])


def get_task_solved(user_id: int, task_id: int) -> bool:
    """Возвращает решенное задание"""

    cur.execute(
        "SELECT * FROM solves WHERE user_id = ? AND task_id = ?", (user_id, task_id))
    return cur.fetchone() is not None


def get_selected_task_id(user_id: int) -> int:
    """Возвращает id задания которые выбрал пользователь"""

    cur.execute("SELECT selected_task_id FROM users WHERE id = ?", (user_id, ))
    return int(cur.fetchone()[0])


def get_user_admin(user_id: int) -> bool:
    """Возвращает является ли пользователь админом"""

    cur.execute("SELECT admin FROM users WHERE id = ?", (user_id, ))
    return bool(cur.fetchone()[0])


def add_user(user_id: int, name: str, admin: bool = False):
    """Добавляет нового пользователя в БД"""

    cur.execute("INSERT INTO users (id, name, admin) VALUES (?, ?, ?)", (user_id, name, admin))
    conn.commit()


def add_task(user_id: int, name: str):
    """Добавляет новое задание в БД"""

    cur.execute(
        """INSERT INTO tasks (owner_user_id, name) 
        VALUES (?, ?)""", (user_id, name))
    conn.commit()


def add_solve(user_id: int, task_id: int):
    """Добавляет новое решение в БД"""

    cur.execute(
        """INSERT INTO solves (user_id, task_id) 
        VALUES (?, ?)""", (user_id, task_id))
    conn.commit()


def delete_task(task_id: int):
    """Удаляет задание из БД"""
    cur.execute("DELETE FROM tasks WHERE id = ? ", (task_id, ))
    conn.commit()


def get_tasks() -> list:
    """Возвращает данные заданий (id, owner_user_id, name, description, flag, points, visible)"""

    cur.execute("SELECT * FROM tasks")
    return cur.fetchall()


def get_users() -> list:
    """Возвращает данные пользователей (id, name, points, admin, selected_task_id)"""

    cur.execute("SELECT * FROM users")
    return cur.fetchall()


def get_scoreboard() -> list:
    """Возвращает рейтинг пользователей"""

    cur.execute("SELECT users.name, SUM(tasks.points) AS score FROM solves JOIN users ON users.id = solves.user_id JOIN tasks ON tasks.id = solves.task_id GROUP BY users.name ORDER BY score DESC")
    return cur.fetchall()


def get_user_score(user_id: int) -> int:
    """Возвращает очки пользователя"""

    cur.execute("SELECT SUM(tasks.points) AS score FROM solves JOIN tasks ON tasks.id = solves.task_id WHERE solves.user_id = ?", (user_id, ))
    return int(cur.fetchone()[0] or 0)


def set_task_name(task_id: int, name: str):
    """Изменяет название задания"""

    cur.execute("UPDATE tasks SET name = ? WHERE id = ?", (name, task_id))
    conn.commit()


def set_task_desc(task_id: int, desc: str):
    """Изменяет описание задания"""

    cur.execute("UPDATE tasks SET description = ? WHERE id = ?",
                (desc, task_id))
    conn.commit()


def set_task_flag(task_id: int, flag: str):
    """Изменяет флаг-ключ задания"""

    cur.execute("UPDATE tasks SET flag = ? WHERE id = ?", (flag, task_id))
    conn.commit()


def set_task_visibility(task_id: int, visible: bool):
    """Изменяет видимость задания"""

    cur.execute("UPDATE tasks SET visible = ? WHERE id = ?",
                (visible, task_id))
    conn.commit()


def set_task_points(task_id: int, points: int):
    """Изменяет количество очков задания"""

    cur.execute("UPDATE tasks SET points = ? WHERE id = ?", (points, task_id))
    conn.commit()


def set_selected_task(user_id: int, task_id: int):
    """Изменить выбранное задание пользователя"""

    cur.execute("UPDATE users SET selected_task_id = ? WHERE id = ?",
                (task_id, user_id))
    conn.commit()


if __name__ == "__main__":
    create_tables()
