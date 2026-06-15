from flask import Flask, render_template, request, redirect
from datetime import date

from database import (
    init_db,
    get_all_messages,
    add_message,
    delete_message,
    get_message_count,
    get_messages_sorted
)

app = Flask(__name__)

init_db()


@app.route('/')
def index():
    messages = get_all_messages()

    total_count = get_message_count()

    today = date.today().isoformat()

    return render_template(
        'index.html',
        messages=messages,
        total_count=total_count,
        today=today
    )


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if name and message:
        add_message(name, message)

    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    delete_message(message_id)

    return redirect('/')

@app.route('/sort/newest')
def sort_newest():

    messages = get_messages_sorted('newest')

    return render_template(
        'index.html',
        messages=messages,
        total_count=get_message_count(),
        today=date.today().isoformat()
    )


@app.route('/sort/oldest')
def sort_oldest():

    messages = get_messages_sorted('oldest')

    return render_template(
        'index.html',
        messages=messages,
        total_count=get_message_count(),
        today=date.today().isoformat()
    )


if __name__ == '__main__':
    app.run(debug=True)