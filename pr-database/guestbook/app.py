from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'guestbook.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM messages ORDER BY id DESC'
    )

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        messages=messages
    )


@app.route('/add', methods=['POST'])
def add_message():
    author = request.form.get('author')
    text = request.form.get('text')

    if author and text:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO messages(author, text)
            VALUES (?, ?)
            ''',
            (author, text)
        )

        conn.commit()
        conn.close()

    return redirect('/')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)