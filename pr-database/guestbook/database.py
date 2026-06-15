import sqlite3
from datetime import date

DATABASE = 'guestbook.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def get_all_messages():
    conn = get_db_connection()

    messages = conn.execute(
        'SELECT * FROM messages ORDER BY created_at DESC, id DESC'
    ).fetchall()

    conn.close()
    return messages


def add_message(name, message):
    conn = get_db_connection()

    conn.execute(
        '''
        INSERT INTO messages (name, message, created_at)
        VALUES (?, ?, ?)
        ''',
        (
            name,
            message,
            date.today().strftime('%Y-%m-%d')
        )
    )

    conn.commit()
    conn.close()

def delete_message(message_id):
    conn = get_db_connection()

    conn.execute(
        'DELETE FROM messages WHERE id = ?',
        (message_id,)
    )

    conn.commit()
    conn.close()


def get_message_count():
    conn = get_db_connection()

    cursor = conn.execute(
        'SELECT COUNT(*) FROM messages'
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_messages_sorted(order='newest'):
    conn = get_db_connection()

    if order == 'oldest':
        messages = conn.execute(
            '''
            SELECT *
            FROM messages
            ORDER BY created_at ASC, id ASC
            '''
        ).fetchall()
    else:
        messages = conn.execute(
            '''
            SELECT *
            FROM messages
            ORDER BY created_at DESC, id DESC
            '''
        ).fetchall()

    conn.close()

    return messages