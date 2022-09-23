import sqlite3

conn = sqlite3.connect("bot.db")
cur = conn.cursor()


def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        points INTEGER NOT NULL,
        admin INTEGER,
        edit_task_id INTEGER,
        FOREIGN KEY (edit_task_id) REFERENCES tasks (id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        flag TEXT NOT NULL,
        points INTEGER NOT NULL,
        visible INTEGER,
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
        path TEXT NOT NULL,
        task_id INTEGER NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )""")
    conn.commit()


def find_user(user_id: int) -> tuple[int, str, int, int, int]:
    """Возвращает данные пользователя"""
    cur.execute(f'''SELECT * FROM users WHERE (id = '{user_id}')''')
    return cur.fetchone()


def find_task(task_id: int) -> tuple:
    cur.execute(f'''SELECT * FROM tasks WHERE (id = '{task_id}')''')
    return cur.fetchone()


def find_task_flag(task_id: int) -> tuple:
    cur.execute(f'''SELECT flag FROM tasks WHERE (id = '{task_id}')''')
    return cur.fetchone()[0]


def get_user_task_id(user_id: int) -> int:
    cur.execute(f'''SELECT edit_task_id FROM users WHERE (id = '{user_id}')''')
    return cur.fetchone()[0]


def add_user(user_id: int, name: str):
    cur.execute(f'''INSERT INTO users (id, name, points) VALUES ('{user_id}', '{name}', '0')''')
    conn.commit()


def add_task(user_id: int, name: str):
    cur.execute(
        f'''INSERT INTO tasks (owner_user_id, name, description, flag, points) VALUES ('{user_id}', '{name}', '', '', 
        '0')''')
    conn.commit()


def delete_task(task_id: int):
    cur.execute(f'''DELETE FROM tasks WHERE id = '{task_id}' ''')
    conn.commit()


def get_tasks() -> list:
    cur.execute(f'''SELECT id ,name, points FROM tasks''')
    return cur.fetchall()


def get_users() -> list:
    cur.execute(f'''SELECT * FROM users''')
    return cur.fetchall()


def edit_task_name(task_id: int, name: str):
    cur.execute(f'''UPDATE tasks SET name = '{name}' WHERE id = '{task_id}' ''')
    conn.commit()


def edit_task_desc(task_id: int, desc: str):
    cur.execute(f'''UPDATE tasks SET description = '{desc}' WHERE id = '{task_id}' ''')
    conn.commit()


def edit_task_flag(task_id: int, flag: str):
    cur.execute(f'''UPDATE tasks SET flag = '{flag}' WHERE id = '{task_id}' ''')
    conn.commit()


def edit_task_points(task_id: int, points: int):
    cur.execute(f'''UPDATE tasks SET points = '{points}' WHERE id = '{task_id}' ''')
    conn.commit()


def set_edit_task(user_id: int, task_id: int):
    cur.execute(f'''UPDATE users SET edit_task_id = '{task_id}' WHERE id = '{user_id}' ''')
    conn.commit()


if __name__ == "__main__":
    create_tables()
