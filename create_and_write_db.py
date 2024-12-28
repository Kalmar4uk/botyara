import sqlite3


def create_db(chat_id):
    """Создаем БД"""
    con = sqlite3.connect(chat_id)
    cur = con.cursor()
    table = """
    CREATE TABLE IF NOT EXISTS user_messages(
        username TEXT,
        message TEXT,
        date_message TEXT
    );

    CREATE TABLE IF NOT EXISTS kaiten_tasks(
        username TEXT,
        tasks TEXT,
        date TEXT
    );
    """
    cur.executescript(table)
    con.close()


def write_message_to_db(user_message, chat_id, kaiten=None):
    """Запись в БД сообщения"""
    con = sqlite3.connect(chat_id)
    cur = con.cursor()
    if kaiten:
        cur.executemany(f"INSERT INTO {kaiten} VALUES(?, ?, ?);", user_message)
    else:
        cur.executemany(
            "INSERT INTO user_messages VALUES(?, ?, ?);",
            user_message
        )
    con.commit()
    con.close()
