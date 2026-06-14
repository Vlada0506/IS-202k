from flask import Flask, render_template, request, redirect

from database import (
    init_db,
    get_all_messages,
    add_message
)

app = Flask(__name__)

init_db()


@app.route('/')
def index():
    messages = get_all_messages()
    return render_template(
        'index.html',
        messages=messages
    )


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if name and message:
        add_message(name, message)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)