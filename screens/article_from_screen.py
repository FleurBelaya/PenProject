from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3


class ArticleFormScreen(Screen):
    def submit_article(self):
        title = self.ids.new_article_title.text.strip()
        content = self.ids.new_article_text.text.strip()
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        author = "Аноним"

        if user_id:
            conn = sqlite3.connect('articles.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT)')
            cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            if row and row[0]:
                author = row[0]
            cursor.execute('INSERT INTO articles (title, content, author) VALUES (?, ?, ?)', (title, content, author))
            conn.commit()
            conn.close()

        self.manager.current = 'articles'
