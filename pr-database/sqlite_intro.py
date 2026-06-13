import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

print("База данных создана и подключена!")

# Создаём таблицу users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

conn.commit()

print("Таблица users создана!")

cursor.execute("DELETE FROM users")
conn.commit()

# Добавляем пользователей
cursor.execute(
    'INSERT INTO users (name, age) VALUES (?, ?)',
    ('Анна', 25)
)

users = [
    ('Иван', 30),
    ('Мария', 22),
    ('Петр', 35)
]

cursor.executemany(
    'INSERT INTO users (name, age) VALUES (?, ?)',
    users
)

conn.commit()

print("Пользователи добавлены!")

# Вывод всех пользователей
cursor.execute('SELECT * FROM users')
all_users = cursor.fetchall()

print("\n--- Все пользователи ---")

for user in all_users:
    print(
        f"id: {user[0]}, "
        f"имя: {user[1]}, "
        f"возраст: {user[2]}"
    )

# Пользователи старше 25
cursor.execute(
    'SELECT * FROM users WHERE age > 25'
)

older_users = cursor.fetchall()

print("\n--- Пользователи старше 25 ---")

for user in older_users:
    print(
        f"id: {user[0]}, "
        f"имя: {user[1]}, "
        f"возраст: {user[2]}"
    )

# Увеличиваем возраст на 1
cursor.execute(
    'UPDATE users SET age = age + 1'
)

conn.commit()

# Проверяем
cursor.execute('SELECT * FROM users')

updated_users = cursor.fetchall()

print("\n--- После увеличения возраста ---")

for user in updated_users:
    print(
        f"id: {user[0]}, "
        f"имя: {user[1]}, "
        f"возраст: {user[2]}"
    )

# Удаляем пользователя с id=2
cursor.execute(
    'DELETE FROM users WHERE id = ?',
    (2,)
)

conn.commit()

cursor.execute('SELECT * FROM users')

remaining_users = cursor.fetchall()

print("\n--- После удаления id=2 ---")

for user in remaining_users:
    print(
        f"id: {user[0]}, "
        f"имя: {user[1]}, "
        f"возраст: {user[2]}"
    )

conn.close()

print("\nСоединение закрыто.")

# PRODUCTS

conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER DEFAULT 0
    )
''')

conn.commit()

print("\nТаблица products создана!")

cursor.execute("DELETE FROM products")
conn.commit()

# Добавляем товары
products = [
    ('Яблоки', 50, 100),
    ('Бананы', 80, 50),
    ('Молоко', 70, 30),
    ('Хлеб', 40, 0),
    ('Сыр', 150, 20)
]

cursor.executemany(
    '''
    INSERT INTO products(name, price, quantity)
    VALUES (?, ?, ?)
    ''',
    products
)

conn.commit()

# Все товары
print("\n--- Все товары ---")

cursor.execute('SELECT * FROM products')

for product in cursor.fetchall():
    print(
        f"{product[0]}. {product[1]} - "
        f"{product[2]} руб, "
        f"в наличии: {product[3]}"
    )

# Товары дешевле 100 рублей
print("\n--- Товары дешевле 100 руб ---")

cursor.execute(
    'SELECT * FROM products WHERE price < 100'
)

for product in cursor.fetchall():
    print(product[1])

# Нет в наличии
print("\n--- Нет в наличии ---")

cursor.execute(
    'SELECT * FROM products WHERE quantity = 0'
)

for product in cursor.fetchall():
    print(product[1])

# Увеличиваем цену
cursor.execute(
    'UPDATE products SET price = price + 10'
)

conn.commit()

print("\n--- После увеличения цены ---")

cursor.execute('SELECT * FROM products')

for product in cursor.fetchall():
    print(
        f"{product[1]} - {product[2]} руб"
    )

# Удаляем дорогие товары
cursor.execute(
    'DELETE FROM products WHERE price > 100'
)

conn.commit()

print("\n--- После удаления дорогих товаров ---")

cursor.execute('SELECT * FROM products')

for product in cursor.fetchall():
    print(product[1])

# Добавляем категорию
try:
    cursor.execute(
        '''
        ALTER TABLE products
        ADD COLUMN category TEXT DEFAULT "другое"
        '''
    )
    conn.commit()
except sqlite3.OperationalError:
    pass

cursor.execute(
    "UPDATE products SET category='фрукты' WHERE name='Яблоки'"
)

cursor.execute(
    "UPDATE products SET category='фрукты' WHERE name='Бананы'"
)

cursor.execute(
    "UPDATE products SET category='молочные' WHERE name='Молоко'"
)

cursor.execute(
    "UPDATE products SET category='выпечка' WHERE name='Хлеб'"
)

conn.commit()

print("\n--- Товары с категориями ---")

cursor.execute(
    'SELECT name, category FROM products'
)

for product in cursor.fetchall():
    print(
        f"{product[0]} -> {product[1]}"
    )

conn.close()