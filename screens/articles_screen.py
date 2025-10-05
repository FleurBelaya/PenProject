from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class ArticlesScreen(Screen):
    def on_enter(self):
        self.load_articles()

    def ensure_articles_schema(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                author TEXT
            )
        ''')
        try:
            cursor.execute('ALTER TABLE articles ADD COLUMN user_id INTEGER')
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute('ALTER TABLE articles ADD COLUMN author TEXT')
        except sqlite3.OperationalError:
            pass

    def load_articles(self):
        container = self.ids.articles_container
        container.clear_widgets()
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        self.ensure_articles_schema(cursor)
        cursor.execute('SELECT id, title, author, user_id FROM articles ORDER BY id DESC')
        articles = cursor.fetchall()
        conn.close()

        app = App.get_running_app()
        current_user_id = getattr(app, 'current_user_id', None)

        for article_id, title, author, user_id in articles:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=8)
            open_btn = Button(text=f"{title} ({author})")
            open_btn.bind(on_press=lambda _btn, id=article_id: self.open_article(id))
            row.add_widget(open_btn)
            if current_user_id and user_id == current_user_id:
                del_btn = Button(text='Удалить', size_hint_x=None, width=100)
                del_btn.bind(on_press=lambda _btn, id=article_id: self.delete_article(id))
                row.add_widget(del_btn)
            container.add_widget(row)

    def open_article_form(self):
        self.manager.current = 'article_form'

    def open_article(self, article_id):
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        self.ensure_articles_schema(cursor)
        cursor.execute('SELECT content FROM articles WHERE id=?', (article_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            content = result[0]
            article_detail_screen = self.manager.get_screen('article_detail')
            article_detail_screen.set_article_text(content)
            self.manager.current = 'article_detail'

    def delete_article(self, article_id):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        self.ensure_articles_schema(cursor)
        cursor.execute('SELECT user_id FROM articles WHERE id = ?', (article_id,))
        row = cursor.fetchone()
        if not row or row[0] != user_id:
            conn.close()
            return
        cursor.execute('DELETE FROM articles WHERE id = ?', (article_id,))
        conn.commit()
        conn.close()
        self.load_articles()
