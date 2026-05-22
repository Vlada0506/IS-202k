from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

FILE_NAME = 'tasks.json'

def load_tasks():
    """Загружает задачи из JSON файла"""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Сохраняет задачи в JSON файл"""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Загружаем задачи при старте
tasks = load_tasks()

@app.route('/')
def index():
    """Главная страница со списком задач"""
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Добавляет новую задачу с текущей датой"""
    new_task = request.form.get('task')
    if new_task and new_task.strip():
        task_data = {
            'text': new_task.strip(),
            'created_at': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'done': False
        }
        tasks.append(task_data)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Удаляет задачу по индексу"""
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

@app.route('/clear_all')
def clear_all():
    """Удаляет все задачи"""
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """Переключает статус выполнения задачи"""
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)