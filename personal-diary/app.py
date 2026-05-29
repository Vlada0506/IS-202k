from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# ============ Функции для работы с JSON ============

def load_entries():
    """Загружает записи из entries.json"""
    if os.path.exists('entries.json'):
        with open('entries.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_entries(entries):
    """Сохраняет записи в entries.json"""
    with open('entries.json', 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

# Загружаем записи
entries = load_entries()

# ============ Маршруты ============

@app.route('/')
def index():
    """Главная страница со списком всех записей"""
    return render_template('index.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    """Страница одной записи"""
    # Ищем запись по id
    for entry in entries:
        if entry['id'] == entry_id:
            return render_template('detail.html', entry=entry)
    return "Запись не найдена", 404

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Добавление новой записи"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if title and content:
            # Генерируем новый id
            new_id = max([e['id'] for e in entries], default=0) + 1
            current_date = datetime.now().strftime('%d.%m.%Y %H:%M')
            
            new_entry = {
                'id': new_id,
                'title': title,
                'content': content,
                'date': current_date
            }
            entries.append(new_entry)
            save_entries(entries)
            
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    """Редактирование записи"""
    # Ищем запись
    entry = None
    for e in entries:
        if e['id'] == entry_id:
            entry = e
            break
    
    if not entry:
        return "Запись не найдена", 404
    
    if request.method == 'POST':
        new_title = request.form.get('title', '').strip()
        new_content = request.form.get('content', '').strip()
        
        if new_title and new_content:
            entry['title'] = new_title
            entry['content'] = new_content
            save_entries(entries)
            
        return redirect(url_for('index'))
    
    return render_template('edit.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    """Удаление записи"""
    global entries
    entries = [e for e in entries if e['id'] != entry_id]
    save_entries(entries)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """Поиск записей по заголовку"""
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered = [e for e in entries if query in e['title'].lower()]
    else:
        filtered = entries
    return render_template('index.html', entries=filtered, search_query=query)

@app.route('/filter/week')
def filter_week():
    """Фильтр записей за последние 7 дней"""
    week_ago = datetime.now() - timedelta(days=7)
    filtered = []
    
    for entry in entries:
        try:
            # Преобразуем дату из строки для сравнения
            entry_date = datetime.strptime(entry['date'], '%d.%m.%Y %H:%M')
            if entry_date >= week_ago:
                filtered.append(entry)
        except:
            # Если дата в неправильном формате, пропускаем
            pass
    
    return render_template('index.html', entries=filtered, filter_type='week')

if __name__ == '__main__':
    app.run(debug=True)