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
    """Главная страница со всеми задачами"""
    return render_template('index.html', tasks=tasks)

@app.route('/active')
def active_tasks():
    """Показывает только активные (невыполненные) задачи"""
    active = [task for task in tasks if not task.get('done', False)]
    return render_template('index.html', tasks=active, filter='active')

@app.route('/completed')
def completed_tasks():
    """Показывает только выполненные задачи"""
    completed = [task for task in tasks if task.get('done', False)]
    return render_template('index.html', tasks=completed, filter='completed')

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

@app.route('/toggle_all_done')
def toggle_all_done():
    """Отмечает все задачи как выполненные"""
    for task in tasks:
        task['done'] = True
    save_tasks(tasks)
    return redirect('/')

@app.route('/toggle_all_undone')
def toggle_all_undone():
    """Снимает отметку выполнения со всех задач"""
    for task in tasks:
        task['done'] = False
    save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Редактирует задачу по индексу"""
    
    # Проверка: существует ли задача с таким индексом
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404
    
    # Получаем задачу для редактирования
    task = tasks[task_id]
    
    if request.method == 'POST':
        # Получаем новый текст из формы
        new_text = request.form.get('task', '').strip()
        
        # Проверка на пустое поле
        if new_text == '':
            return render_template('edit.html', task=task, message="❌ Текст не может быть пустым!")
        
        # Проверка: изменился ли текст
        old_text = task['text']
        if new_text == old_text:
            return render_template('edit.html', task=task, message="⚠️ Ничего не изменено. Текст остался прежним.")
        
        # Сохраняем новый текст
        tasks[task_id]['text'] = new_text
        save_tasks(tasks)
        
        return redirect('/')
    
    # GET-запрос: показываем форму редактирования
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)