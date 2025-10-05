import sqlite3

conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

# Таблица слов для упражнения three_in_row
cursor.execute('''
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL
)
''')

# Таблица стихов для poetic_trace
cursor.execute('''
CREATE TABLE IF NOT EXISTS poems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line TEXT NOT NULL
)
''')

# Таблица вопросов для why
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL
)
''')

# Пример данных (если нужно)
cursor.execute("INSERT INTO words (word) VALUES ('книга'), ('дом'), ('кот'), ('солнце')")
cursor.execute("INSERT INTO poems (line) VALUES ('Мир в красках утра'), ('Тишина в лесу')")
cursor.execute("INSERT INTO questions (question) VALUES ('Почему небо голубое?'), ('Зачем мы спим?')")

conn.commit()
conn.close()


