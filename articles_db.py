import sqlite3

conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    favorite_genre TEXT,
    daily_goal INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    profile_color TEXT DEFAULT 'white'  -- Начальный цвет фона профиля
)
''')

conn.commit()
conn.close()


