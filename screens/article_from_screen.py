from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3

class ArticleFormScreen(Screen):
    def submit_article(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return

        title = self.ids.new_article_title.text.strip()
        text = self.ids.new_article_text.text.strip()

        if not title or not text:
            print("Заголовок и текст не могут быть пустыми")
            return

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                author TEXT
            )
        ''')
        cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        author = row[0].strip() if row and row[0] else 'аноним'
        cursor.execute(
            'INSERT INTO articles (user_id, title, content, author) VALUES (?, ?, ?, ?)',
            (user_id, title, text, author)
        )
        conn.commit()
        conn.close()

        self.ids.new_article_title.text = ''
        self.ids.new_article_text.text = ''

        app.root.current = 'articles'

